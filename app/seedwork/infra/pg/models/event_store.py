from uuid import UUID

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from seedwork.infra.pg.models import BaseOrm
from seedwork.infra.pg.models.common import CreatedAtMixin


class StoredEventOrm(
    BaseOrm,
    CreatedAtMixin,
):
    __tablename__ = "stored_events"

    event_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    event_type: Mapped[str]
    event_version: Mapped[int]
    aggregate_id: Mapped[UUID] = mapped_column(index=True)
    aggregate_version: Mapped[int]
    payload: Mapped[dict] = mapped_column(JSON)
