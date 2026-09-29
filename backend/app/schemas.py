from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.models.product import ProductCategory
from app.models.order import PaymentMethod, OrderStatus


class ProductOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    metal_type: str | None = None
    category: ProductCategory
    image_url: str
    in_stock: bool
    stock_quantity: int

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    metal_type: str | None = None
    category: ProductCategory
    image_url: str
    in_stock: bool = True
    stock_quantity: int = 0


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    metal_type: str | None = None
    category: ProductCategory | None = None
    image_url: str | None = None
    in_stock: bool | None = None
    stock_quantity: int | None = None


class OrderItemIn(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_phone: str
    shipping_address: str
    city: str
    payment_method: PaymentMethod
    items: list[OrderItemIn]


class OrderOut(BaseModel):
    id: int
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: str
    city: str
    items: list
    total: float
    payment_method: PaymentMethod
    status: OrderStatus
    created_at: datetime

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class StockAlertCreate(BaseModel):
    product_id: int
    email: EmailStr


class StockAlertOut(BaseModel):
    id: int
    product_id: int
    email: str
    notified: bool

    class Config:
        from_attributes = True