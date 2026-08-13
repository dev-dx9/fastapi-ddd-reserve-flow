from fastapi import APIRouter

from .resource_group import router as resource_group_router

router = APIRouter()

router.include_router(resource_group_router)
