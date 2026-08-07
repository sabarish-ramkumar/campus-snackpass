import os
import random
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import or_
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db

# Creates tables on startup if they don't exist yet. Fine for a project
# this size; a larger team project would use Alembic migrations instead
# so schema changes are tracked and reversible.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campus SnackPass API")

# CORS: the frontend and backend are deployed as separate services
# (Vercel + Render), so the browser will make cross-origin requests.
# FRONTEND_URL is set as an env var on Render once you know your
# Vercel URL; localhost is kept so local dev keeps working too.
_origins = ["http://localhost:5173", os.getenv("FRONTEND_URL", "")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o for o in _origins if o],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_unique_token(db: Session) -> str:
    """
    Generates a short, human-friendly order token like 'SP-4F2K9'.
    Characters 0/O and 1/I are excluded on purpose — they're easy to
    misread at a noisy counter. Checked against the DB in a loop so
    a collision (rare, but possible) can never produce a duplicate.
    """
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    while True:
        code = "".join(random.choices(alphabet, k=5))
        token = f"SP-{code}"
        if not db.query(models.Order).filter(models.Order.token == token).first():
            return token


def serialize_order(order: models.Order, db: Session) -> dict:
    """
    Builds the nested order response by hand. OrderItem doesn't store
    the item's name directly (that lives on MenuItem), so this looks
    each one up rather than relying on Pydantic to auto-map a join.
    """
    items_out = []
    for oi in order.items:
        menu_item = (
            db.query(models.MenuItem).filter(models.MenuItem.id == oi.menu_item_id).first()
        )
        items_out.append(
            {
                "menu_item_id": oi.menu_item_id,
                "name": menu_item.name if menu_item else "Item no longer on menu",
                "quantity": oi.quantity,
                "unit_price": oi.unit_price,
            }
        )
    return {
        "id": order.id,
        "token": order.token,
        "status": order.status,
        "total": order.total,
        "created_at": order.created_at,
        "items": items_out,
    }


@app.get("/")
def root():
    return {"status": "ok", "service": "campus-snackpass-api"}


@app.get("/menu-items", response_model=List[schemas.MenuItemOut])
def list_menu_items(
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.MenuItem).filter(models.MenuItem.is_active == True)  # noqa: E712

    if category and category.lower() != "all":
        query = query.filter(models.MenuItem.category == category)

    if search:
        like = f"%{search}%"
        query = query.filter(
            or_(models.MenuItem.name.ilike(like), models.MenuItem.description.ilike(like))
        )

    return query.order_by(models.MenuItem.category, models.MenuItem.name).all()


@app.get("/menu-items/{item_id}", response_model=schemas.MenuItemOut)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item


@app.get("/categories", response_model=List[str])
def list_categories(db: Session = Depends(get_db)):
    rows = (
        db.query(models.MenuItem.category)
        .filter(models.MenuItem.is_active == True)  # noqa: E712
        .distinct()
        .order_by(models.MenuItem.category)
        .all()
    )
    return [r[0] for r in rows]


@app.post("/orders", response_model=schemas.OrderOut, status_code=201)
def create_order(order_in: schemas.OrderCreate, db: Session = Depends(get_db)):
    if not order_in.items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")

    total = 0.0
    resolved_lines = []  # (menu_item, quantity) pairs, looked up server-side

    # Security-relevant: the request only ever contains menu_item_id +
    # quantity. We look up the real price ourselves and compute the
    # total here — never from a price/total the client sent — so a
    # tampered request body can't produce a discounted order.
    for line in order_in.items:
        menu_item = (
            db.query(models.MenuItem)
            .filter(models.MenuItem.id == line.menu_item_id, models.MenuItem.is_active == True)  # noqa: E712
            .first()
        )
        if not menu_item:
            raise HTTPException(
                status_code=404,
                detail=f"Menu item {line.menu_item_id} not found or unavailable",
            )
        total += menu_item.price * line.quantity
        resolved_lines.append((menu_item, line.quantity))

    order = models.Order(
        token=generate_unique_token(db),
        status="pending",
        total=round(total, 2),
    )
    db.add(order)
    db.flush()  # assigns order.id without committing yet, so child rows can reference it

    for menu_item, quantity in resolved_lines:
        db.add(
            models.OrderItem(
                order_id=order.id,
                menu_item_id=menu_item.id,
                quantity=quantity,
                unit_price=menu_item.price,
            )
        )

    db.commit()
    db.refresh(order)

    return serialize_order(order, db)


@app.get("/orders/{token}", response_model=schemas.OrderOut)
def get_order_by_token(token: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.token == token).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return serialize_order(order, db)


# --- Admin-style CRUD on menu items (no auth layer yet — see README) ---
# The assessment brief calls for CRUD on menu items and/or orders.
# These three complete that requirement for menu items. There's no
# login/auth gate on them, which is called out explicitly in the
# README as a known, intentional scope cut for the 2-day timeline —
# not an oversight.


@app.post("/menu-items", response_model=schemas.MenuItemOut, status_code=201)
def create_menu_item(item: schemas.MenuItemOut, db: Session = Depends(get_db)):
    # id from the input is ignored — the database assigns it.
    new_item = models.MenuItem(
        name=item.name,
        category=item.category,
        price=item.price,
        description=item.description,
        image_url=item.image_url,
        is_active=True,
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.put("/menu-items/{item_id}", response_model=schemas.MenuItemOut)
def update_menu_item(item_id: int, updated: schemas.MenuItemOut, db: Session = Depends(get_db)):
    item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    item.name = updated.name
    item.category = updated.category
    item.price = updated.price
    item.description = updated.description
    item.image_url = updated.image_url
    db.commit()
    db.refresh(item)
    return item


@app.delete("/menu-items/{item_id}", status_code=204)
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    # Soft delete — see the comment on MenuItem.is_active in models.py
    # for why this isn't db.delete(item).
    item.is_active = False
    db.commit()
    return None
