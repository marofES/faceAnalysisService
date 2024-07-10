from fastapi import FastAPI
import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from sqlalchemy import text 
from src.auth.router import router as auth_router
from src.config import settings
from src.database import sessionmanager

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if settings.log_level == "DEBUG" else logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()

app = FastAPI(lifespan=lifespan, title=settings.project_name, docs_url="/api/docs")
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/check-db-connection")
async def check_db_connection():
    try:
        async with sessionmanager.session() as session:
            await session.execute(text("SELECT 1"))  # Use text() to declare SQL expression
        return {"status": "Database connection successful!"}
    except Exception as e:
        return {"status": f"Failed to connect to database: {str(e)}"}
# Routers

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
