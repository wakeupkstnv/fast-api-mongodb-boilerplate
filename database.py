from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

class DataBase:
    client: AsyncIOMotorClient = None
    db = None
    reviews = None

db = DataBase()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.mongodb_url)
    db.db = db.client[settings.database_name]
    db.reviews = db.db.reviews  

async def close_mongo_connection():
    if db.client:
        db.client.close()
    db.client = None
    db.db = None
    db.reviews = None

def get_database() -> DataBase:
    return db