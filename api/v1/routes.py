from fastapi import APIRouter
from api.v1.controllers.order.order_controller import router
v1_router = APIRouter()

v1_router.include_router(router)