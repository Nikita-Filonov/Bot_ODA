from typing import List, Dict

from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton


def ensure_message_valid(message: Message, mapping: List[Dict[str, str]], key='name') -> bool:
    return any(message.text == item[key] for item in mapping)


def build_keyboard(mapping: List[Dict[str, str]], key='name') -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(*[KeyboardButton(item[key]) for item in mapping])
