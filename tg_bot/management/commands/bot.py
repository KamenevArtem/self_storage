import logging


from django.conf import settings
from django.core.management.base import BaseCommand

from telegram.ext import Filters
from telegram.ext import Updater
from telegram.ext import MessageHandler

from tg_bot.middleware import auth_middleware


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        updater = Updater(settings.TG_BOT_TOKEN, use_context=True)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(
            MessageHandler(
                Filters.all,
                auth_middleware
            ),
            group=-1
        )

        updater.start_polling(clean=True)
        updater.idle()
