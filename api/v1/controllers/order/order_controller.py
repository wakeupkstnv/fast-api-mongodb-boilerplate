from fastapi import APIRouter, Depends
from typing import List
from database import get_database, DataBase
from api.v1.schema.order.order_schema import OrderInDB
from api.v1.services.order.order_services import OrderService

router = APIRouter(prefix="/order", tags=["orders"])

async def get_order_service(db: DataBase = Depends(get_database)) -> OrderService:
    return OrderService(db)

@router.get("/", response_model=List[OrderInDB])
async def get_all_orders(
    service: OrderService = Depends(get_order_service)
) -> List[OrderInDB]:
    return await service.get_all()

@router.get("/random", response_model=OrderInDB)
async def get_random_order(
    service: OrderService = Depends(get_order_service)
) -> OrderInDB:
    return await service.get_random()

@router.get("/{user_id}", response_model=OrderInDB)
async def get_order_by_user_id(
    user_id: str,
    service: OrderService = Depends(get_order_service)
) -> OrderInDB:
    return await service.get_by_user_id(user_id)