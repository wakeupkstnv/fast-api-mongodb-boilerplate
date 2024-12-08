from bson import ObjectId
from database import DataBase
from api.v1.models.map.establishments_model import EstablishmentInDB
from fastapi import HTTPException

class ItemNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Item not found")

class DatabaseInitializationError(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail="Database not initialized")

def process_establishment_item(item):
    try:
        return EstablishmentInDB(**item, id=str(item["_id"])) if "_id" in item else EstablishmentInDB(**item)
    except Exception as e:
        print(f"Error processing item: {item}")
        print(f"Detailed error: {e}")
        return None

async def get_all_establishments(db: DataBase):
    if db.reviews is None:
        raise DatabaseInitializationError()

    items = await db.reviews.find().to_list(length=None)
    if not items:
        raise ItemNotFoundError()

    establishments = [process_establishment_item(item) for item in items]
    establishments = list(filter(None, establishments))
    return establishments

async def get_establishments_by_page(db: DataBase, page: int, limit: int):
    skip = (page - 1) * limit
    if db.reviews is None:
        raise DatabaseInitializationError()

    items = await db.reviews.find().skip(skip).limit(limit).to_list(length=None)
    if not items:
        raise ItemNotFoundError()

    establishments = [process_establishment_item(item) for item in items]
    establishments = list(filter(None, establishments))  
    return establishments

async def get_establishment_by_oid(db: DataBase, item_id: str):
    if db.reviews is None:
        raise DatabaseInitializationError()

    item = await db.reviews.find_one({"_id": ObjectId(item_id)})
    if item is None:
        raise ItemNotFoundError()

    return EstablishmentInDB(**item, id=str(item["_id"]))

async def get_establishment_by_2gis_id(db: DataBase, two_gis_id: str):
    if db.reviews is None:
        raise DatabaseInitializationError()

    item = await db.reviews.find_one({"two_gis_id": two_gis_id})
    if item is None:
        raise ItemNotFoundError()

    return EstablishmentInDB(**item, id=str(item["_id"]))

async def search_establishments_by_title(db: DataBase, establishment_title: str):
    if db.reviews is None:
        raise DatabaseInitializationError()

    items = await db.reviews.aggregate([
        {
            "$search": {
                "text": {
                    "query": establishment_title,
                    "path": "title",
                    "fuzzy": {"maxEdits": 2}  # Не более двух ошибок
                }
            }
        },
        {"$project": {"title": 1, "_id": 1}}  # Проекцируем только нужные поля
    ]).to_list(length=None)

    if not items:
        raise ItemNotFoundError()

    establishments = [process_establishment_item(item) for item in items]
    establishments = list(filter(None, establishments))  # Убираем None из результатов
    return establishments
