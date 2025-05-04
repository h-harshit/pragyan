from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base
from models.mixins import TimeStampMixin


class ClientConnectionConfig(Base, TimeStampMixin):
    __tablename__ = "client_connection_config"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(nullable=False)
    engine_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    conn_string: Mapped[str] = mapped_column(nullable=False)
    db_name: Mapped[str] = mapped_column(nullable=False)
    dialect: Mapped[str] = mapped_column(nullable=False)
