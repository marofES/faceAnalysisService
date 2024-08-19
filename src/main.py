from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pathlib import Path

import json
import base64

# from src.auth.router import router as auth_router
from src.tools.router import router as tools_router
# from src.database import engine, Base


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to the frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(tools_router, prefix="/tools", tags=["tools"])

# Mount the static directory to serve CSS and other static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Load the initial base64 image from face_def.json
    with open("D:/faceService/src/face_image_default.json", "r") as file:
        data = json.load(file)
        initial_base64_image = data.get("face_detect", "")

    return templates.TemplateResponse("index.html", {"request": request, "initial_base64_image": initial_base64_image})

@app.get("/face-docs/", response_class=HTMLResponse)
async def custom_docs(request: Request):
    return templates.TemplateResponse("docs.html", {"request": request})
