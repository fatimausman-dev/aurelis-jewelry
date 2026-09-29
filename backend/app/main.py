from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.db import Base, engine
from app.models import product, order, push_subscription  # noqa: F401
from app.routers import products, orders, stock_alerts, auth, uploads

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Jewelry Brand API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(orders.router)
app.include_router(stock_alerts.router)
app.include_router(auth.router)
app.include_router(uploads.router)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.get("/")
def root():
    return {"status": "ok", "message": "Jewelry Brand API is running"}