from telegram import Update
from telegram.ext import CallbackContext

from tg_bot.models import UserProfile

from tg_bot.handlers.conversations.employee_conv import employee_conversation
from tg_bot.handlers.conversations.customer_conv import customer_conversation


def auth_middleware(
        update: Update,
        context: CallbackContext
):
    user_id = update.message.from_user.id
    users_in_db = UserProfile.objects.all()
    users_tg_id = [user.tg_id for user in users_in_db if user.tg_id]

    if user_id in users_tg_id:
        context.dispatcher.add_handler(employee_conversation)
    else:
        context.dispatcher.add_handler(customer_conversation)
