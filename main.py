import logging

import telebot
from telebot.types import Message

from keyboard import regions_markup, variants_markup, variants, regions
from orm.controllers import get_sub_variants, init_user, save_user_answer, get_user_payload
from utils import ensure_message_valid, build_keyboard, serialize_contact_information

TOKEN = "5343039631:AAE7AXTAvO2dVr5gFNwgAwp1yB0SKGAYFNY"
bot = telebot.TeleBot(TOKEN)
cat = "⬇️Оберіть Категорію⬇️ :"


@bot.message_handler(commands=["start"], chat_types=['private'])
def start(message: Message):
    logging.warning(f'Start command received from {message.from_user.id}')

    bot.send_message(
        message.chat.id,
        "Доброго дня,{0.first_name}👋\n🔍Оберіть Громаду 🏡 :".format(message.from_user),
        reply_markup=regions_markup
    )
    init_user(message)


@bot.message_handler(content_types=["text"], chat_types=['private'])
def text(message: Message):
    logging.warning(f'Handling text content type from user {message.from_user.id}')

    if ensure_message_valid(message, mapping=regions):
        save_user_answer(message, region=message.text)
        bot.send_message(message.from_user.id, cat, reply_markup=variants_markup)
        bot.register_next_step_handler(message, handle_variants)


def handle_variants(message: Message):
    if ensure_message_valid(message, mapping=variants):
        if message.text == "↩ПОВЕРНУТИСЬ":
            start(message)
            return

        save_user_answer(message, variant=message.text)

        sub_variants = get_sub_variants(message.text)
        print('sub_variants', sub_variants)
        if sub_variants:
            sub_variants_markup = build_keyboard(mapping=sub_variants)

            bot.send_message(message.from_user.id, text="Оберіть:", reply_markup=sub_variants_markup)
            bot.register_next_step_handler(message, handle_sub_variants, sub_variants=sub_variants)
            return

        handle_payload(message)
    else:
        start(message)
        return


def handle_payload(message: Message):
    payload = get_user_payload(message)
    logging.warning(f'Sending payload to user {message.from_user.id}')

    bot.send_message(message.from_user.id, text=serialize_contact_information(payload), parse_mode='html')
    start(message)


def handle_sub_variants(message: Message, sub_variants):
    logging.warning(f'handling sub variants for user {message.from_user.id}')

    save_user_answer(message, sub_variant=message.text)
    if ensure_message_valid(message, mapping=sub_variants):
        handle_payload(message)
    else:
        start(message)
        return


bot.polling(non_stop=True, timeout=150)
