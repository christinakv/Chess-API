from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Integer, String, ForeignKey

class Base(DeclarativeBase):
    __abstract__ = True
