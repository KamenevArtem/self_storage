from telegram import Update
from telegram.ext import CallbackContext


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Прошу прощения, данной команды я не знаю"
    )
