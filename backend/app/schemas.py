from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class MenuItemOut(BaseModel):
    id: int
    name: str
    category: str
    price: float
    description: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True  # lets Pydantic read straight from the ORM object


class OrderItemIn(BaseModel):
    menu_item_id: int
    quantity: int = Field(gt=0)  # rejects 0 or negative quantities at the boundary


class OrderCreate(BaseModel):
    items: List[OrderItemIn]


class OrderItemOut(BaseModel):
    menu_item_id: int
    name: str
    quantity: int
    unit_price: float


class OrderOut(BaseModel):
    id: int
    token: str
    status: str
    total: float
    created_at: datetime
    items: List[OrderItemOut]
