import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Bot
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from tg_bot.handlers.conversations.employee_conv import employee_conversation
from tg_bot.handlers import unknown


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        bot = Bot(
            token=settings.TOKEN,
        )
        updater = Updater(
            bot=bot,
        )
        dispatcher = updater.dispatcher

        # TODO регистрируем хендлеры в зависимости от того кто пишет боту

        dispatcher.add_handler(employee_conversation)
        unknown_command_handler = MessageHandler(Filters.command, unknown)
        dispatcher.add_handler(unknown_command_handler)
        updater.start_polling(clean=True)
        updater.idle()
