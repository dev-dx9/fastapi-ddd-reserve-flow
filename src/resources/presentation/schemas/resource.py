from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateResourceRequest(BaseModel):
    name: str
    qty: int


class UpdateResourceRequest(BaseModel):
    name: str
    qty: int


class ResourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    resource_group_id: UUID
    name: str
    qty: int
