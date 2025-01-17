from bson import ObjectId
from typing import List, Optional
from fastapi import HTTPException
from database import DataBase
from api.v1.schema.order.order_schema import OrderInDB


class OrderException:
    class ItemNotFound(HTTPException):
        def __init__(self, message: str = "Item not found"):
            super().__init__(status_code=404, detail=message)

    class DatabaseError(HTTPException):
        def __init__(self, message: str = "Database error occurred"):
            super().__init__(status_code=500, detail=message)


class OrderService:
    def __init__(self, db: DataBase):
        self.db = db
        if self.db.orders is None:
            raise OrderException.DatabaseError("Orders collection not initialized")

    def _process_order(self, item: dict) -> Optional[OrderInDB]:
        try:
            return OrderInDB(**item, id=str(item["_id"])) if "_id" in item else OrderInDB(**item)
        except Exception as e:
            print(f"Error processing order: {e}")
            return None

    async def get_all(self) -> List[OrderInDB]:
        try:
            items = await self.db.orders.find().to_list(length=None)
            if not items:
                raise OrderException.ItemNotFound("No orders found")

            orders = [self._process_order(item) for item in items]
            return [order for order in orders if order is not None]
        except Exception as e:
            raise OrderException.DatabaseError(f"Error fetching orders: {str(e)}")

    async def get_by_id(self, order_id: str) -> OrderInDB:
        try:
            item = await self.db.orders.find_one({"_id": ObjectId(order_id)})
            if item is None:
                raise OrderException.ItemNotFound(f"Order with id {order_id} not found")

            return self._process_order(item)
        except Exception as e:
            raise OrderException.DatabaseError(f"Error fetching order: {str(e)}")

    async def get_by_user_id(self, user_id: str) -> OrderInDB:
        try:
            item = await self.db.orders.find_one({"user_id": user_id})
            if item is None:
                raise OrderException.ItemNotFound(f"Order for user {user_id} not found")

            return self._process_order(item)
        except Exception as e:
            raise OrderException.DatabaseError(f"Error fetching order: {str(e)}")

    async def get_random(self) -> OrderInDB:
        try:
            pipeline = [
                {"$sample": {"size": 1}}
            ]

            result = await self.db.orders.aggregate(pipeline).to_list(length=1)
            if not result:
                raise OrderException.ItemNotFound("No orders available")

            return self._process_order(result[0])
        except Exception as e:
            raise OrderException.DatabaseError(f"Error fetching random order: {str(e)}")