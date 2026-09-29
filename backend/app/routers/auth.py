import os
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

router = APIRouter(prefix="/admin", tags=["admin"])


class LoginRequest(BaseModel):
    password: str


class LoginResponse(BaseModel):
    token: str


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    if not ADMIN_PASSWORD or not ADMIN_TOKEN:
        raise HTTPException(status_code=500, detail="Admin credentials not configured on server")
    if payload.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Incorrect password")
    return LoginResponse(token=ADMIN_TOKEN)


def verify_admin(x_admin_token: str = Header(...)):
    """
    Dependency used to protect admin-only endpoints.
    Every protected route requires an X-Admin-Token header matching ADMIN_TOKEN.
    """
    if not ADMIN_TOKEN or x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing admin token")
    return True