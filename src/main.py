from fastapi import FastAPI
from src.auth.router import router as auth_router
from src.database import engine, Base

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
