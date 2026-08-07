"""
Run with:  python -m app.seed
Populates the menu_items table. Safe to re-run — it skips seeding if
the table already has rows, so it won't create duplicates.
"""

from .database import Base, engine, SessionLocal
from . import models

MENU_ITEMS = [
    {"name": "Masala Chai", "category": "Beverages", "price": 15,
     "description": "Hot spiced milk tea"},
    {"name": "Cold Coffee", "category": "Beverages", "price": 40,
     "description": "Iced coffee with milk and sugar"},
    {"name": "Lemon Soda", "category": "Beverages", "price": 25,
     "description": "Fresh lime soda, sweet or salted"},
    {"name": "Buttermilk", "category": "Beverages", "price": 20,
     "description": "Spiced chilled buttermilk"},
    {"name": "Samosa", "category": "Snacks", "price": 15,
     "description": "Crispy fried pastry with spiced potato filling"},
    {"name": "Veg Puff", "category": "Snacks", "price": 20,
     "description": "Flaky pastry with vegetable filling"},
    {"name": "French Fries", "category": "Snacks", "price": 60,
     "description": "Crispy salted fries"},
    {"name": "Chilli Paneer", "category": "Snacks", "price": 80,
     "description": "Spicy tossed paneer, Indo-Chinese style"},
    {"name": "Veg Fried Rice", "category": "Meals", "price": 70,
     "description": "Wok-tossed rice with mixed vegetables"},
    {"name": "Chicken Biryani", "category": "Meals", "price": 120,
     "description": "Fragrant rice with spiced chicken"},
    {"name": "Veg Thali", "category": "Meals", "price": 90,
     "description": "Rice, roti, dal, sabzi, and curd"},
    {"name": "Masala Dosa", "category": "Meals", "price": 55,
     "description": "Crispy rice crepe with spiced potato filling"},
    {"name": "Gulab Jamun", "category": "Desserts", "price": 30,
     "description": "Soft milk dumplings in sugar syrup"},
    {"name": "Ice Cream", "category": "Desserts", "price": 40,
     "description": "Vanilla scoop with chocolate sauce"},
    {"name": "Fruit Custard", "category": "Desserts", "price": 35,
     "description": "Chilled custard with mixed fruits"},
]


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(models.MenuItem).count()
        if existing > 0:
            print(
                f"menu_items already has {existing} rows — skipping seed. "
                f"Delete rows in Neon's SQL editor first if you want to reseed."
            )
            return
        for item in MENU_ITEMS:
            db.add(models.MenuItem(**item, is_active=True))
        db.commit()
        print(f"Seeded {len(MENU_ITEMS)} menu items.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
