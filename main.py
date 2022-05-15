import telebot
from telebot.types import Message

from bot.handlers import start_handler, text_handler
from settings import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"], chat_types=['private'])
def start(message: Message):
    start_handler(message, bot)


@bot.message_handler(content_types=["text"], chat_types=['private'])
def text(message: Message):
    text_handler(message, bot)


bot.polling(non_stop=True, timeout=150)
