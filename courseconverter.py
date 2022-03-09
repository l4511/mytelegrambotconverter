import telebot
from extensions import APIExceptions, Convertor
from config import TOKEN, exchanges
import traceback

bot=telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def startwork(message:telebot.types.Message):
    bot.send_message(message.chat.id, f'Здравствуйте,Вас приветствует Бот-помощник.'
                          f'Мы поможем вам узнать цену интересующей вас валюты.'
                          f'Для начала работы введите количество и валюту которую вы хотите перевести.'
                          f'После введите интересующую Вас валюту. Можете использовать /help'
                   )
@bot.message_handler(commands=['help'])
def startwork(message:telebot.types.Message):
    bot.send_message(message.chat.id, f'Введите количество валюты,которую Вы хотите перевести. '
                                      f' Введите валюту, которую Вы хотите перевести.'
                                      f' Введите валюту которую Вы хотите получить.' 
                                      f' Для просмотра доступных валют введите /values'
                                             )
@bot.message_handler(commands=['values'])
def values(message:telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text,i))
    bot.send_message( message.chat.id, text)

@bot.message_handler(content_types=['text'])
def converter(message:telebot.types.Message):
    value=message.text.split(' ')
    try:
        if len(value) != 3:
            raise APIExceptions('Неверное количество параметров!')
        else:
            answer = Convertor.get_price(*value)
    except APIExceptions as e:
        bot.reply_to(message,f'Ошибка в команде:\n{e}')
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message,f'Неизвестная ошибка:\n {e}')
    else:
        bot.send_message(message.chat.id,answer)

bot.polling(none_stop=True)
