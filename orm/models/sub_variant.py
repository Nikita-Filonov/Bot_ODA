from sqlalchemy import Column, Integer, ForeignKey, String

from orm.models.base import BaseModel


class SubVariant(BaseModel):
    __tablename__ = 'sub_variant'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), comment='Название варианта', default=None)
    variant_id = Column(Integer, ForeignKey('variant.id'), comment='Вариант', default=None)
