from sqlalchemy.orm import Mapped

from src.database import Base
from src.database_types import (
    uuid_pk,
)


class ResourceGroupModel(Base):
    __tablename__ = 'resource_groups'

    id: Mapped[uuid_pk]
    name: Mapped[str]
