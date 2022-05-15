from sqlalchemy import Column, Integer, String

from orm.models.base import BaseModel


class User(BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, comment='ID пользователя Telegram')
    region = Column(String(200), default=None, comment='Регион выбранный юзером')
    variant = Column(String(200), default=None, comment='Вариант выбранный юзером')
    sub_variant = Column(String(200), default=None, comment='Под вариант выбранный юзером')
