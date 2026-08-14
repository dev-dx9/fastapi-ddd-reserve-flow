from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.resources.infrastructure.models import (
    ResourceGroupModel,
)
from src.resources.presentation.schemas import (
    CreateResourceGroupRequest,
)


class SQLAlchemyResourceGroupRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(
        self,
    ) -> list[ResourceGroupModel]:
        models = (
            await self._session.scalars(
                select(ResourceGroupModel),
            )
        ).all()

        return list(models)

    async def add(
        self,
        request: CreateResourceGroupRequest,
    ) -> ResourceGroupModel:
        model = ResourceGroupModel(
            name=request.name,
        )

        self._session.add(model)

        return model

    async def get_by_id(
        self,
        resource_group_id: UUID,
    ) -> ResourceGroupModel | None:
        return await self._session.get(
            ResourceGroupModel,
            resource_group_id,
        )
