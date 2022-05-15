from typing import List, Union

from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

from orm.models import Payload, Variant, SubVariant, Region


def is_message_valid(message: Message, mapping: List[Union[Variant, SubVariant, Region]]) -> bool:
    """
    :param message: Обект сообщения ``telebot.types.Message``
    :param mapping: Список с любым из объектов ``Variant``, ``SubVariant``, ``Region``
    :return: Возвращает булево значение True/False
    """
    return any(message.text == item.name for item in mapping)


def build_keyboard(mapping: List[Union[Variant, SubVariant, Region]], **kwargs) -> ReplyKeyboardMarkup:
    """
    :param mapping: Список с любым из объектов ``Variant``, ``SubVariant``, ``Region``
    :param kwargs: Любые кейворд аргументы для ``telebot.types.ReplyKeyboardMarkup``
    :return: Возвращает ``telebot.types.ReplyKeyboardMarkup``

    Обертка для составление моркапа кнопок
    """
    return ReplyKeyboardMarkup(resize_keyboard=True, **kwargs).add(*[KeyboardButton(item.name) for item in mapping])


def serialize_contact_information(payloads: List[Payload]) -> str:
    """
    :param payloads: Список с информацией ``Payload``
    :return: Возвращает строку с HTML шаблоном

    Используется, чтобы форматировать и переводить список
    с объектами ``Payload`` в человеко читабельный вид
    """
    if not payloads:
        return '<strong>Мы не смогли ничего найти</strong>'

    information = ''.join([
        f"""
        <em>Телефон</em>: {payload.phone}
        <em>Адрес</em>: {payload.address}
        <em>Электронная почта</em>: {payload.email}
        {f'<em>Дполнительная информация</em>: {payload.details}' if payload.details else ''}
        """
        for payload in payloads
    ])

    return """<strong>Контактна інформація:</strong>\n""" + information
