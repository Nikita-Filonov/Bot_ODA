from typing import Union, List, Tuple

from orm.database import Base


def serializer(rows: Union[Base, List[Base], Tuple[Base]], exclude=None) -> Union[dict, List[dict]]:
    """
    :param rows: List of declarative base object or single declarative base object
    :param exclude: Fields to exclude. Should be provided as list of strings
    :return: Returns serialized result of declarative base objects
    """
    safe_exclude = exclude or []

    if isinstance(rows, (list, tuple)):
        return [serializer(row, exclude=safe_exclude) for row in rows]

    return {
        column.name: getattr(rows, column.name)
        for column in rows.__table__.columns
        if (column.name not in safe_exclude)
    }
