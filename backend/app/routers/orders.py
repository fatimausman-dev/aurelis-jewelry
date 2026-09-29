from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.order import Order
from app.models.product import Product
from app.schemas import OrderCreate, OrderOut, OrderStatusUpdate
from app.email_utils import send_order_confirmation_email, send_admin_out_of_stock_email
from app.routers.auth import verify_admin

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=list[OrderOut], dependencies=[Depends(verify_admin)])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).order_by(Order.created_at.desc()).all()


@router.put("/{order_id}/status", response_model=OrderOut, dependencies=[Depends(verify_admin)])
def update_order_status(order_id: int, status_in: OrderStatusUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status_in.status
    db.commit()
    db.refresh(order)
    return order


@router.post("/", response_model=OrderOut)
def create_order(
    order_in: OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    if not order_in.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    items_snapshot = []
    total = 0.0
    newly_out_of_stock = []

    for item in order_in.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if not product.in_stock or product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"'{product.name}' is out of stock")

        line_total = product.price * item.quantity
        total += line_total
        items_snapshot.append({
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": item.quantity,
        })

        product.stock_quantity -= item.quantity
        if product.stock_quantity <= 0:
            product.in_stock = False
            newly_out_of_stock.append(product)

    order = Order(
        customer_name=order_in.customer_name,
        customer_email=order_in.customer_email,
        customer_phone=order_in.customer_phone,
        shipping_address=order_in.shipping_address,
        city=order_in.city,
        items=items_snapshot,
        total=total,
        payment_method=order_in.payment_method,
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    background_tasks.add_task(send_order_confirmation_email, order)
    for product in newly_out_of_stock:
        background_tasks.add_task(send_admin_out_of_stock_email, product)

    return order


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order