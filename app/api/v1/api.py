from fastapi import APIRouter

from app.api.v1.endpoints import example, health

api_router = APIRouter()
api_router.include_router(example.router, prefix="/example")
api_router.include_router(health.router, prefix="/health")
