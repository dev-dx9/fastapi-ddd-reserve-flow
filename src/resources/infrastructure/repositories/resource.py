from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.resources.infrastructure.models.resource import (
    ResourceModel,
)
from src.resources.presentation.schemas.resource import (
    CreateResourceRequest,
)


class SQLAlchemyResourceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(
        self,
        resource_group_id: UUID,
    ) -> list[ResourceModel]:
        models = (
            await self._session.scalars(
                select(ResourceModel).where(
                    ResourceModel.resource_group_id == resource_group_id,
                )
            )
        ).all()

        return list(models)

    async def add(
        self,
        resource_group_id: UUID,
        request: CreateResourceRequest,
    ) -> ResourceModel:
        model = ResourceModel(
            resource_group_id=resource_group_id,
            name=request.name,
            qty=request.qty,
        )

        self._session.add(model)

        return model

    async def get_by_id(
        self,
        resource_id: UUID,
        resource_group_id: UUID,
    ) -> ResourceModel | None:
        return await self._session.scalar(
            select(ResourceModel).where(
                ResourceModel.id == resource_id,
                ResourceModel.resource_group_id == resource_group_id,
            ),
        )
