from uuid import UUID

from sqlalchemy import UUID as SA_UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.resources.infrastructure.common import (
    uuid_pk,
)


class ResourceModel(Base):
    __tablename__ = 'resources'

    id: Mapped[uuid_pk]
    resource_group_id: Mapped[UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        ForeignKey('resource_groups.id'),
    )
    name: Mapped[str]
    qty: Mapped[int]
