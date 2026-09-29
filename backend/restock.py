"""
Marks a product back in stock and emails everyone who signed up for an alert.
Usage: python restock.py <product_id> <quantity>
Example: python restock.py 8 10
"""

import sys
from app.db import SessionLocal
from app.models.product import Product
from app.models.push_subscription import StockAlert
from app.email_utils import send_stock_alert_email


def restock(product_id: int, quantity: int):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            print(f"No product with id {product_id}")
            return

        product.stock_quantity = quantity
        product.in_stock = quantity > 0
        db.commit()
        print(f"'{product.name}' restocked to {quantity} units.")

        alerts = (
            db.query(StockAlert)
            .filter(StockAlert.product_id == product_id, StockAlert.notified == False)  # noqa: E712
            .all()
        )
        for alert in alerts:
            send_stock_alert_email(alert.email, product)
            alert.notified = True
        db.commit()
        print(f"Notified {len(alerts)} waiting customer(s).")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python restock.py <product_id> <quantity>")
        sys.exit(1)
    restock(int(sys.argv[1]), int(sys.argv[2]))