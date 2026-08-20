from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from src.dependencies import SessionDep
from src.resources.infrastructure.repositories import (
    SQLAlchemyResourceGroupRepository,
    SQLAlchemyResourceRepository,
)
from src.resources.presentation.schemas import (
    CreateResourceRequest,
    ResourceResponse,
    UpdateResourceRequest,
)

router = APIRouter(
    prefix='/resource-groups',
    tags=['Resources'],
)


@router.get(
    '/{resource_group_id}/resources',
    response_model=list[ResourceResponse],
)
async def get_resources(
    resource_group_id: UUID,
    session: SessionDep,
) -> list[ResourceResponse]:
    resource_group_repository = SQLAlchemyResourceGroupRepository(session)
    resource_group = await resource_group_repository.get_by_id(
        resource_group_id,
    )

    if resource_group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Resource group not found',
        )

    repository = SQLAlchemyResourceRepository(session)
    models = await repository.get_all(resource_group_id)

    return [ResourceResponse.model_validate(model) for model in models]


@router.post(
    '/{resource_group_id}/resources',
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_resource(
    resource_group_id: UUID,
    request: CreateResourceRequest,
    session: SessionDep,
) -> ResourceResponse:
    resource_group_repository = SQLAlchemyResourceGroupRepository(session)
    resource_group = await resource_group_repository.get_by_id(
        resource_group_id,
    )

    if resource_group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Resource group not found',
        )

    repository = SQLAlchemyResourceRepository(session)
    model = await repository.add(
        resource_group_id,
        request,
    )

    await session.commit()
    await session.refresh(model)

    return ResourceResponse.model_validate(model)


@router.get(
    '/{resource_group_id}/resources/{resource_id}',
    response_model=ResourceResponse,
)
async def get_resource(
    resource_group_id: UUID,
    resource_id: UUID,
    session: SessionDep,
) -> ResourceResponse:
    resource_group_repository = SQLAlchemyResourceGroupRepository(session)
    resource_group = await resource_group_repository.get_by_id(
        resource_group_id,
    )

    if resource_group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Resource group not found',
        )

    repository = SQLAlchemyResourceRepository(session)
    model = await repository.get_by_id(
        resource_id,
        resource_group_id,
    )

    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Resource not found',
        )

    return ResourceResponse.model_validate(model)


@router.patch(
    '/{resource_group_id}/resources/{resource_id}',
    response_model=ResourceResponse,
)
async def update_resource(
    resource_group_id: UUID,
    resource_id: UUID,
    request: UpdateResourceRequest,
    session: SessionDep,
) -> ResourceResponse:
    resource_group_repository = SQLAlchemyResourceGroupRepository(session)
    resource_group = await resource_group_repository.get_by_id(
        resource_group_id,
    )

    if resource_group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Resource group not found',
        )

    repository = SQLAlchemyResourceRepository(session)
    model = await repository.get_by_id(
        resource_id,
        resource_group_id,
    )

    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Resource not found',
        )

    for field, value in request.model_dump(
        exclude_unset=True,
    ).items():
        setattr(model, field, value)

    await session.commit()
    await session.refresh(model)

    return ResourceResponse.model_validate(model)


@router.delete(
    '/{resource_group_id}/resources/{resource_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_resource(
    resource_group_id: UUID,
    resource_id: UUID,
    session: SessionDep,
) -> None:
    resource_group_repository = SQLAlchemyResourceGroupRepository(session)
    resource_group = await resource_group_repository.get_by_id(
        resource_group_id,
    )

    if resource_group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Resource group not found',
        )

    repository = SQLAlchemyResourceRepository(session)
    model = await repository.get_by_id(resource_id, resource_group_id)

    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Resource not found',
        )

    await session.delete(model)
    await session.commit()
