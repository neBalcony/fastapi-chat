from app.api.routes import user
from fastapi import APIRouter

from app.api.routes import chat

api_router = APIRouter(prefix="/api")
api_router.include_router(chat.router)
api_router.include_router(user.router)