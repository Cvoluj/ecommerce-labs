from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
