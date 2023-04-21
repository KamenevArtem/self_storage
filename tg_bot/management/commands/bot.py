import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from ...customer_handlers import conv_handler, unknown

from telegram import Bot
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater


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
        dispatcher.add_handler(conv_handler)
        unknown_command_handler = MessageHandler(Filters.command, unknown)
        dispatcher.add_handler(unknown_command_handler)
        updater.start_polling()
        updater.idle()