from fastapi import APIRouter

from .endpoints import url

api_router = APIRouter()
api_router.include_router(url.router, prefix="/url", tags=["url"])
