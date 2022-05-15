from sqlalchemy import Column, Integer, String

from orm.models.base import BaseModel


class Region(BaseModel):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), comment='Название региона', default=None)
