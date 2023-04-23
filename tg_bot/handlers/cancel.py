from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler


def cancel(update, _):
    update.message.reply_text(
        'Спасибо за уделенное Вами время'
        'Если хотите продолжить работу введите команду'
        '/start',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
