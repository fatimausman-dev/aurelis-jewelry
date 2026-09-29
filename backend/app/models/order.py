import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, JSON
from app.db import Base


class PaymentMethod(str, enum.Enum):
    cod = "cod"
    safepay = "safepay"


class OrderStatus(str, enum.Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    shipping_address = Column(String, nullable=False)
    city = Column(String, nullable=False)

    items = Column(JSON, nullable=False)
    total = Column(Float, nullable=False)

    payment_method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)

    created_at = Column(DateTime, default=datetime.utcnow)