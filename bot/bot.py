# bot/bot.py
import telebot
from telebot import types
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

class BotView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        json_str = request.body.decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return HttpResponse('OK')

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    user_markup.row('Амир Темур', 'Жанна Дарк', 'Гитлер')
    bot.send_message(message.from_user.id, 'Выберите личность:', reply_markup=user_markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Амир Темур':
        bot.send_message(message.chat.id, 'Информация о Амире Темуре: ...')
    elif message.text == 'Жанна Дарк':
        bot.send_message(message.chat.id, 'Информация о Жанне Дарк: ...')
    elif message.text == 'Гитлер':
        bot.send_message(message.chat.id, 'Информация о Гитлере: ...')
    else:
        bot.send_message(message.chat.id, 'Выберите личность из списка.')

