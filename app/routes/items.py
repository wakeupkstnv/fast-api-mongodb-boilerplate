from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.models.item import Item, ItemInDB
from app.db.mongodb import get_database, DataBase

router = APIRouter()

@router.post("/items/", response_model=ItemInDB)
async def create_item(item: Item, db: DataBase = Depends(get_database)):
    try:
        if db.items is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        result = await db.items.insert_one(item.dict())
        if not result.acknowledged:
            raise HTTPException(status_code=500, detail="Failed to create item")
        
        item_in_db = ItemInDB(**item.dict(), id=str(result.inserted_id))
        return item_in_db
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/items/{item_id}", response_model=ItemInDB)
async def read_item(item_id: str, db: DataBase = Depends(get_database)):
    try:
        if db.items is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        item = await db.items.find_one({"_id": ObjectId(item_id)})
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        
        return ItemInDB(**item, id=str(item["_id"]))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")