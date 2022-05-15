from typing import List, Dict

from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

from orm.models import Payload


def ensure_message_valid(message: Message, mapping: List[Dict[str, str]], key='name') -> bool:
    return any(message.text == item[key] for item in mapping)


def build_keyboard(mapping: List[Dict[str, str]], key='name') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(*[KeyboardButton(item[key]) for item in mapping])


def serialize_contact_information(payloads: List[Payload]) -> str:
    information = ''.join([
        f"""
        <em>Телефон</em>: {payload.phone}
        <em>Адрес</em>: {payload.address}
        <em>Электронная почта</em>: {payload.email}
        """
        for payload in payloads
    ])

    return """<strong>Контактна інформація:</strong>\n""" + information
