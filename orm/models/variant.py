from sqlalchemy import Column, Integer, String

from orm.models.base import BaseModel


class Variant(BaseModel):
    __tablename__ = 'variant'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), comment='Название варианта', default=None)
