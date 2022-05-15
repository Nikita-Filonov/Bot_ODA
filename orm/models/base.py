from typing import Optional, List, Union

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload, Session

from orm.database import Base


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def get(cls, session: Session, load: Union[list, tuple, None] = None, **kwargs) -> Optional['BaseModel']:
        query = select(cls).filter_by(**kwargs)

        if load:
            for table in load:
                query = query.options(selectinload(table))

        result = session.execute(query)
        return result.scalars().first()

    @classmethod
    def filter(
            cls,
            session: Session,
            select_values: Union[list, tuple, None] = None,
            order_by: Union[list, tuple, None] = None,
            slice_query: Union[list, tuple, None] = None,
            load: Union[list, tuple, None] = None,
            **kwargs
    ) -> List['BaseModel']:
        query = select(select_values or cls).filter_by(**kwargs)
        if order_by:
            query = query.order_by(*order_by)

        if slice_query:
            query = query.slice(*slice_query)

        if load:
            for table in load:
                query = query.options(selectinload(table))

        result = session.execute(query)
        return result.scalars().all()

    @classmethod
    def create(cls, session: Session, **kwargs) -> 'BaseModel':
        model = cls(**kwargs)
        session.add(model)
        session.commit()

        return model

    @classmethod
    def delete(cls, session: Session, **kwargs) -> None:
        model = cls.get(session, **kwargs)

        if model is None:
            raise NotImplementedError('Row is not found')

        session.delete(model)
        session.commit()

    @classmethod
    def update(cls, session: Session, entity_id, entity_key='id', **kwargs) -> None:
        where = {entity_key: entity_id}
        query = update(cls).filter_by(**where).values(**kwargs)
        session.execute(query)
        session.commit()
