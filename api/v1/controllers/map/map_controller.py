from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from typing import List
from database import get_database, DataBase
from api.v1.models.map.establishments_model import EstablishmentInDB
from api.v1.services.map.map_services import (
    get_all_establishments,
    get_establishments_by_page,
    get_establishment_by_oid,
    get_establishment_by_2gis_id,
    search_establishments_by_title,
)

router = APIRouter()

@router.get("/establishments/get_all", response_model=List[EstablishmentInDB])
async def get_all_items(db: DataBase = Depends(get_database)):
    try:
        return await get_all_establishments(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/establishments/", response_model=List[EstablishmentInDB])
async def get_items(db: DataBase = Depends(get_database), page: int = 1, limit: int = 10):
    try:
        return await get_establishments_by_page(db, page, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/establishments/by_object_id/{establishments_id}", response_model=EstablishmentInDB)
async def get_item_by_oid(item_id: str, db: DataBase = Depends(get_database)):
    try:
        return await get_establishment_by_oid(db, item_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/establishments/by_two_gis_id/{two_gis_id}", response_model=EstablishmentInDB)
async def get_item_by_2gis(two_gis_id: str, db: DataBase = Depends(get_database)):
    try:
        return await get_establishment_by_2gis_id(db, two_gis_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/establishments/by_title/{establishment_title}", response_model=List[EstablishmentInDB])
async def get_item_by_name(establishment_title: str, db: DataBase = Depends(get_database)):
    try:
        return await search_establishments_by_title(db, establishment_title)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
