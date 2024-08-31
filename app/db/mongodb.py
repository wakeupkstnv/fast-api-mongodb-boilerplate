from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class DataBase:
    client: AsyncIOMotorClient = None
    db = None
    items = None

db = DataBase()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.mongodb_url)
    db.db = db.client[settings.database_name]
    db.items = db.db.items  # Инициализация коллекции items

async def close_mongo_connection():
    if db.client:
        db.client.close()
    db.client = None
    db.db = None
    db.items = None

def get_database() -> DataBase:
    return db