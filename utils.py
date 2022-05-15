from typing import List, Union

from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

from orm.models import Payload, Variant, SubVariant, Region


def is_message_valid(message: Message, mapping: List[Union[Variant, SubVariant, Region]]) -> bool:
    return any(message.text == item.name for item in mapping)


def build_keyboard(mapping: List[Union[Variant, SubVariant, Region]], **kwargs) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True, **kwargs).add(*[KeyboardButton(item.name) for item in mapping])


def serialize_contact_information(payloads: List[Payload]) -> str:
    if not payloads:
        return '<strong>Мы не смогли ничего найти</strong>'

    information = ''.join([
        f"""
        <em>Телефон</em>: {payload.phone}
        <em>Адрес</em>: {payload.address}
        <em>Электронная почта</em>: {payload.email}
        """
        for payload in payloads
    ])

    return """<strong>Контактна інформація:</strong>\n""" + information
