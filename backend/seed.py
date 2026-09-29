"""
One-off script to insert sample products for local development/testing.
Run with: python seed.py
Safe to run multiple times — it clears existing products first.
"""

from app.db import SessionLocal, Base, engine
from app.models.product import Product, ProductCategory

Base.metadata.create_all(bind=engine)

SAMPLE_PRODUCTS = [
    dict(name="Aurelia Ring", description="A quietly sculptural gold ring, shaped by hand.",
         price=1480, metal_type="18K Yellow Gold", category=ProductCategory.rings,
         image_url="/images/category-rings.jpg", in_stock=True, stock_quantity=12),
    dict(name="Celeste Pendant", description="A single champagne diamond suspended on a fine chain.",
         price=1920, metal_type="18K Gold, Champagne Diamond", category=ProductCategory.necklaces,
         image_url="/images/category-necklaces.jpg", in_stock=True, stock_quantity=8),
    dict(name="Orbit Hoops", description="Classic hoop earrings with a soft, hand-polished finish.",
         price=860, metal_type="18K Yellow Gold", category=ProductCategory.earrings,
         image_url="/images/category-earrings.jpg", in_stock=True, stock_quantity=20),
    dict(name="Twine Cuff", description="A sculptural open cuff bracelet, twisted by hand.",
         price=1150, metal_type="18K Yellow Gold", category=ProductCategory.bracelets,
         image_url="/images/category-bracelets.jpg", in_stock=True, stock_quantity=6),
    dict(name="Teardrop Pendant", description="A minimalist gold teardrop with a single set stone.",
         price=780, metal_type="18K Gold", category=ProductCategory.pendants,
         image_url="/images/category-pendants.jpg", in_stock=True, stock_quantity=15),
    dict(name="Signature Set", description="Matching necklace and earring set for special occasions.",
         price=2400, metal_type="18K Gold, Diamond", category=ProductCategory.sets,
         image_url="/images/category-sets.jpg", in_stock=True, stock_quantity=4),
    dict(name="Eternal Band", description="A classic wedding band, quietly detailed with pave stones.",
         price=1650, metal_type="18K Yellow Gold", category=ProductCategory.wedding,
         image_url="/images/category-wedding.jpg", in_stock=True, stock_quantity=10),
    dict(name="Signet Ring", description="A bold, understated signet ring with a single flush stone.",
         price=980, metal_type="18K Yellow Gold", category=ProductCategory.mens,
         image_url="/images/category-mens.jpg", in_stock=False, stock_quantity=0),
]


def run():
    db = SessionLocal()
    try:
        db.query(Product).delete()
        for item in SAMPLE_PRODUCTS:
            db.add(Product(**item))
        db.commit()
        count = db.query(Product).count()
        print(f"Seeded {count} products.")
    finally:
        db.close()


if __name__ == "__main__":
    run()