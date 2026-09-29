from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.product import Product
from app.models.push_subscription import StockAlert
from app.schemas import StockAlertCreate, StockAlertOut

router = APIRouter(prefix="/stock-alerts", tags=["stock-alerts"])


@router.post("/", response_model=StockAlertOut)
def create_stock_alert(alert_in: StockAlertCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == alert_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.in_stock:
        raise HTTPException(status_code=400, detail="Product is already in stock")

    existing = (
        db.query(StockAlert)
        .filter(
            StockAlert.product_id == alert_in.product_id,
            StockAlert.email == alert_in.email,
            StockAlert.notified == False,  # noqa: E712
        )
        .first()
    )
    if existing:
        return existing

    alert = StockAlert(product_id=alert_in.product_id, email=alert_in.email)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert