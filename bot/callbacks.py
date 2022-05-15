import logging
from typing import Callable, List

from telebot import TeleBot
from telebot.types import Message

from bot.keyboard import variants
from orm.controllers import get_sub_variants, save_user_answer, get_user_payload
from orm.models import SubVariant
from settings import BACK_ACTION, SUB_VARIANT_REPLY
from bot.utils import is_message_valid, build_keyboard, serialize_contact_information


def variants_callback(message: Message, bot: TeleBot, start_handler: Callable):
    if not is_message_valid(message, mapping=variants):
        start_handler(message, bot=bot)
        return

    if message.text == BACK_ACTION:
        start_handler(message, bot=bot)
        return

    save_user_answer(message, variant=message.text)

    sub_variants = get_sub_variants(message.text)

    if sub_variants:
        sub_variants_markup = build_keyboard(mapping=sub_variants)

        bot.send_message(message.from_user.id, text=SUB_VARIANT_REPLY, reply_markup=sub_variants_markup)
        bot.register_next_step_handler(
            message, sub_variants_callback, sub_variants=sub_variants, bot=bot, start_handler=start_handler)
        return

    payload_callback(message, bot=bot, start_handler=start_handler)


def payload_callback(message: Message, bot: TeleBot, start_handler: Callable):
    logging.warning(f'Sending payload to user {message.from_user.id}')
    payload = get_user_payload(message)

    bot.send_message(message.from_user.id, text=serialize_contact_information(payload), parse_mode='html')
    start_handler(message, bot=bot)


def sub_variants_callback(message: Message, sub_variants: List[SubVariant], bot: TeleBot, start_handler: Callable):
    logging.warning(f'handling sub variants for user {message.from_user.id}')

    save_user_answer(message, sub_variant=message.text)
    if not is_message_valid(message, mapping=sub_variants):
        start_handler(message, bot=bot)
        return

    payload_callback(message, bot=bot, start_handler=start_handler)
