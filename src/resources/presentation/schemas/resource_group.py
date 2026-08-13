from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateResourceGroupRequest(BaseModel):
    name: str


class UpdateResourceGroupRequest(BaseModel):
    name: str


class ResourceGroupResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
