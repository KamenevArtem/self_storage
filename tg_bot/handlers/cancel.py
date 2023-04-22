from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler


def cancel(update, _):
    update.message.reply_text(
        'Спасибо за уделенное Вами время',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
