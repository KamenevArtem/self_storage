from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import models

from telegram import Bot
from telegram import Update
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from telegram.utils.request import Request


def log_errors(function):
    def inner(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as error:
            raise error
    return inner


@log_errors
def start(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Оставить вещи", callback_data='leave'),
            InlineKeyboardButton("Забрать вещи", callback_data='take'),
        ],
        [InlineKeyboardButton("Узнать правила хранения", callback_data='rules')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Что Вас интересует?', reply_markup=reply_markup)


@log_errors
def call_leave_staff(update: Update, context: CallbackContext):
    keyboard = [
        InlineKeyboardButton("Оформить заказ", callback_data='4'),
        InlineKeyboardButton("Вернуться в стартовое меню", callback_data='5'),
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Хотели бы Вы оставить заявку на хранение вещей?', reply_markup=reply_markup)


@log_errors
def handle_buttons(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == 'leave':
        query.answer()
        query.edit_message_text(text='Спасибо, что выбираете нас!')
    if query.data == 'take':
        query.edit_message_text(text='Какой из заказов Вас интересует?')
    if query.data == 'rules':
        query.edit_message_text(text=f'Правила хранения (FAQ)')


@log_errors
def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Прошу прощения, данной команды я не знаю"
        )


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
        )
        updater = Updater(
            bot=bot,
        )
        dispatcher = updater.dispatcher
        
        start_command_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_command_handler)
        unknown_command_handler = MessageHandler(Filters.command, unknown)
        dispatcher.add_handler(unknown_command_handler)
        
        dispatcher.add_handler(CallbackQueryHandler(handle_buttons))
        
        dispatcher.add_handler(MessageHandler(Filters.text, call_leave_staff))

        updater.start_polling()
        updater.idle()