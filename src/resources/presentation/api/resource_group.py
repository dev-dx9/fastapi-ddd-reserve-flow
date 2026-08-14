from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.database import AsyncSessionFactory
from src.resources.infrastructure.repositories import (
    SQLAlchemyResourceGroupRepository,
)
from src.resources.presentation.schemas import (
    CreateResourceGroupRequest,
    ResourceGroupResponse,
    UpdateResourceGroupRequest,
)

router = APIRouter(
    prefix='/resource-groups',
    tags=['Resource Groups'],
)


@router.get(
    '',
    response_model=list[ResourceGroupResponse],
)
async def get_resource_groups() -> list[ResourceGroupResponse]:
    async with AsyncSessionFactory() as session:
        repository = SQLAlchemyResourceGroupRepository(session)
        models = await repository.get_all()

        return [ResourceGroupResponse.model_validate(model) for model in models]


@router.post(
    '',
    response_model=ResourceGroupResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_resource_group(
    request: CreateResourceGroupRequest,
) -> ResourceGroupResponse:
    async with AsyncSessionFactory() as session:
        repository = SQLAlchemyResourceGroupRepository(session)
        model = await repository.add(request)

        await session.commit()
        await session.refresh(model)

        return ResourceGroupResponse.model_validate(model)


@router.get(
    '/{resource_group_id}',
    response_model=ResourceGroupResponse,
)
async def get_resource_group(
    resource_group_id: UUID,
) -> ResourceGroupResponse:
    async with AsyncSessionFactory() as session:
        repository = SQLAlchemyResourceGroupRepository(session)
        model = await repository.get_by_id(resource_group_id)

        if model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Resource group not found',
            )

        return ResourceGroupResponse.model_validate(model)


@router.patch(
    '/{resource_group_id}',
    response_model=ResourceGroupResponse,
)
async def update_resource_group(
    resource_group_id: UUID,
    request: UpdateResourceGroupRequest,
) -> ResourceGroupResponse:
    async with AsyncSessionFactory() as session:
        repository = SQLAlchemyResourceGroupRepository(session)
        model = await repository.get_by_id(resource_group_id)

        if model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Resource group not found',
            )

        model.name = request.name

        await session.commit()
        await session.refresh(model)

        return ResourceGroupResponse.model_validate(model)


@router.delete(
    '/{resource_group_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_resource_group(
    resource_group_id: UUID,
) -> None:
    async with AsyncSessionFactory() as session:
        repository = SQLAlchemyResourceGroupRepository(session)
        model = await repository.get_by_id(resource_group_id)

        if model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Resource group not found',
            )

        await session.delete(model)
        await session.commit()
