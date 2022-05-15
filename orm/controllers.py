from typing import List, Dict, Union, Optional

from sqlalchemy import select
from telebot.types import Message

from orm.database import db_session
from orm.models import Region, Variant, Payload, SubVariant, User
from orm.utils import serializer


def get_regions() -> List[Dict[str, Union[int, str]]]:
    regions = Region.filter(session=db_session)
    return serializer(regions)


def get_variants() -> List[Dict[str, Union[int, str]]]:
    variants = Variant.filter(session=db_session)
    return serializer(variants)


def get_sub_variants(variant_name: str) -> List[Dict[str, Union[int, str]]]:
    query = select(SubVariant).join(Variant).filter(Variant.name == variant_name)
    query_result = db_session.execute(query).scalars().all()
    return serializer(query_result)


def get_variant_payload(
        region_name: str,
        variant_name: str,
        sub_variant_name: Optional[str]
) -> List[Dict[str, Union[int, str]]]:
    query = select(Payload) \
        .outerjoin(Region) \
        .outerjoin(Variant) \
        .outerjoin(SubVariant, Payload.sub_variant_id == SubVariant.id) \
        .filter(Region.name == region_name, Variant.name == variant_name, SubVariant.name == sub_variant_name)
    query_result = db_session.execute(query).scalars().all()
    return serializer(query_result, exclude=['variant_id', 'region_id', 'sub_variant_id'])


def init_user(message: Message):
    user = User.get(db_session, user_id=message.from_user.id)

    if user:
        User.update(db_session, entity_id=user.id, region=None, variant=None, sub_variant=None)
    else:
        User.create(db_session, user_id=message.from_user.id)
