from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import UUID as SA_UUID
from sqlalchemy.orm import mapped_column

uuid_pk = Annotated[
    UUID,
    mapped_column(
        SA_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    ),
]

# created_at = Annotated[...]
# updated_at = Annotated[...]
