from fastapi import APIRouter

from .events.handlers import router


v1_router = APIRouter(prefix="/v1")
v1_router.include_router(router)
