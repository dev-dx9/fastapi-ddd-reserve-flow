from fastapi import APIRouter

from .resource import router as resource_router
from .resource_group import router as resource_group_router

router = APIRouter()

router.include_router(resource_group_router)
router.include_router(resource_router)
