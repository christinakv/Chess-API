from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    __abstract__ = True

    __tablename__ : Mapped[str]
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)