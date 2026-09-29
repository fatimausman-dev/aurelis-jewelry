import enum
from sqlalchemy import Column, Integer, String, Float, Enum, Boolean
from app.db import Base


class ProductCategory(str, enum.Enum):
    rings = "rings"
    necklaces = "necklaces"
    earrings = "earrings"
    bracelets = "bracelets"
    pendants = "pendants"
    sets = "sets"
    wedding = "wedding"
    mens = "mens"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    metal_type = Column(String, nullable=True)
    category = Column(Enum(ProductCategory), nullable=False)
    image_url = Column(String, nullable=False)
    in_stock = Column(Boolean, default=True)
    stock_quantity = Column(Integer, default=0)