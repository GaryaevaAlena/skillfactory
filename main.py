import telebot

from config import *
from extensions import Convertor, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "Добрый день. Чтобы начать работу введите команду /convert. Чтобы посмотреть доступные для конвертации валюты введите команду /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(commands=["convert"])
def values(message: telebot.types.Message):
    text = "Выберите валюту для конвертации:"
    bot.reply_to(message, text)
    bot.register_next_step_handler(message, base_handler)


def base_handler(message: telebot.types.Message):
    base = message.text.strip()
    text = "Выберите валюту в которую нужно осуществить конвертацию:"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, quote_handler, base)

def quote_handler(message: telebot.types.Message, base):
    quote = message.text.strip()
    text = "Выберите количество конвертируемой валюты:"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)


def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        new_price = Convertor.get_price(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка конвертации: \n {e} ")
    else:
        text = f"Цена {amount} {base} в {quote} : {new_price}"
        bot.reply_to(message, text)



bot.polling()





