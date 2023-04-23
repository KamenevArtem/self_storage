import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Bot
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from tg_bot.handlers.conversations.employee_conv import employee_conversation
from tg_bot.handlers.conversations.customer_conv import customer_conversation
from tg_bot.handlers import unknown


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        customer_bot = Bot(
            token=settings.CUSTOMER_TOKEN,
        )
        customer_updater = Updater(
            bot=customer_bot
        )
        customer_dispatcher = customer_updater.dispatcher
        customer_dispatcher.add_handler(customer_conversation)
        unknown_command_handler = MessageHandler(Filters.command, unknown)
        customer_dispatcher.add_handler(unknown_command_handler)
        customer_updater.start_polling(clean=True)
        employer_bot = Bot(
            token=settings.EMPLOYER_TOKEN,
        )
        employer_updater = Updater(
            bot=employer_bot
        )
        employer_dispatcher = employer_updater.dispatcher
        employer_dispatcher.add_handler(employee_conversation)
        unknown_command_handler = MessageHandler(Filters.command, unknown)
        employer_dispatcher.add_handler(unknown_command_handler)
        employer_updater.start_polling(clean=True)
        employer_updater.idle()
        customer_updater.idle()