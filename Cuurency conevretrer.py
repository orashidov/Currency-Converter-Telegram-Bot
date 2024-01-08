import telebot
from extensions import CryptoConverter, APIException
from config import TOKEN, API_KEY

bot = telebot.TeleBot(TOKEN)
crypto_converter = CryptoConverter(api_key=API_KEY)

keys = {
    'Евро': 'EUR',
    'Доллар': 'USD',
    'Рубль': 'RUB'
}

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.reply_to(message,
                 'Данный бот поможет вам узнать текущую конвертационную цену на следующие три валюты: ЕВРО, ДОЛЛАР И РУБЛЬ.\n'
                 'Чтобы использовать этого бота, отправьте ему сообщение в следующем формате: <название валюты> <название второй валюты> <количество>.\n\n'
                 'Пример: RUB USD 25000'
                 '\n\nСписок доступных валют можно увидеть, отправив команду /values.')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text += f'\n{key}'
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert_currency(message: telebot.types.Message):
    values = message.text.split(" ")

    if len(values) != 3:
        bot.reply_to(message, 'Неправильный формат. Используйте: <название валюты> <название второй валюты> <количество>.\n'
                              'Пример: RUB USD 25000')
    else:
        base, quote, amount = values
        try:
            final_amount = crypto_converter.get_price(base, quote, amount)
            bot.send_message(
                message.chat.id, f"Конвертация: {amount} {base} в {quote} составляет {final_amount}")
        except APIException as error:
            bot.send_message(message.chat.id, 'Неправильный формат ввода данных. Используйте: <название валюты> <название второй валюты> <количество>.\n Пример: RUB USD 25000\n' + f"Ошибка: {error}")

bot.polling(none_stop=True)