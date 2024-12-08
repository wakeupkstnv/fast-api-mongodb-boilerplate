from fastapi import APIRouter
from api.v1.routes import v1_router

global_router = APIRouter()
global_router.include_router(v1_router, prefix='/v1')
