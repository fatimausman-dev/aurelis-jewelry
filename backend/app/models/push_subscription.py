from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.db import Base


class StockAlert(Base):
    __tablename__ = "stock_alerts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    email = Column(String, nullable=False)
    notified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)