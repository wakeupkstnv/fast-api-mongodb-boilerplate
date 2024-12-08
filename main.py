from fastapi import FastAPI
from api.global_router import global_router
from database import close_mongo_connection, connect_to_mongo

app = FastAPI()

app.include_router(global_router, prefix='/api')

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()
    

@app.get("/")
async def root():
    return {"ping": "pong"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)