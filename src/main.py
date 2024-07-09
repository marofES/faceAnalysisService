from fastapi import FastAPI
from src.auth.router import auth_router
from src.database import engine
from src.models import Base

# Create the FastAPI app instance
app = FastAPI()

# Create the database tables asynchronously
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Include the auth router
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# Example root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello World"}
