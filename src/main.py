from fastapi import FastAPI

from src.resources.presentation.api import router as resource_router

app = FastAPI()

app.include_router(resource_router)
