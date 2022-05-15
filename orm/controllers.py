from typing import List, Optional

from sqlalchemy import select
from telebot.types import Message

from orm.database import db_session
from orm.models import Region, Variant, Payload, SubVariant, User


def get_regions() -> List[Region]:
    return Region.filter(session=db_session)


def get_variants() -> List[Variant]:
    return Variant.filter(session=db_session)


def get_sub_variants(variant_name: str) -> List[SubVariant]:
    query = select(SubVariant).join(Variant).filter(Variant.name == variant_name)
    return db_session.execute(query).scalars().all()


def get_variant_payload(region_name: str, variant_name: str, sub_variant_name: Optional[str]) -> List[Payload]:
    query = select(Payload) \
        .outerjoin(Region) \
        .outerjoin(Variant) \
        .outerjoin(SubVariant, Payload.sub_variant_id == SubVariant.id) \
        .filter(Region.name == region_name, Variant.name == variant_name, SubVariant.name == sub_variant_name)
    return db_session.execute(query).scalars().all()


def init_user(message: Message) -> None:
    user = User.get(db_session, user_id=message.from_user.id)

    if user:
        User.update(db_session, entity_id=user.id, region=None, variant=None, sub_variant=None)
    else:
        User.create(db_session, user_id=message.from_user.id)


def save_user_answer(message: Message, **kwargs) -> None:
    User.update(db_session, entity_id=message.from_user.id, entity_key='user_id', **kwargs)


def get_user_payload(message: Message) -> List[Payload]:
    user = User.get(db_session, user_id=message.from_user.id)
    return get_variant_payload(
        region_name=user.region,
        variant_name=user.variant,
        sub_variant_name=user.sub_variant
    )
