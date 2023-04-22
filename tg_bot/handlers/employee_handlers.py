from telegram import Update
from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from telegram.ext import CallbackContext

from tg_bot.states import EmployeeState
from tg_bot import services, tmp_data
from tg_bot.models import Order


def start_for_employer(update: Update, _):
    kbd_layout = [
        'Список заказов',
        'Список просроченных заказов',
        'Пользователи пришедшие по рекламе'
    ]

    update.message.reply_text(
        text='Что вас интересует?',
        reply_markup=services.create_tg_keyboard_markup(kbd_layout, 2)
    )

    return EmployeeState.ACTION


def get_all_orders(update: Update, context: CallbackContext):
    context.user_data['action'] = update.message.text
    orders = Order.objects.all()
    kbd_layout = ['Бокс {}'.format(order.box) for order in orders]

    update.message.reply_text(
        text='Список активных заказов',
        reply_markup=services.create_tg_keyboard_markup(kbd_layout)
    )

    return EmployeeState.ORDERS


def get_failed_orders(update: Update, context: CallbackContext):
    context.user_data['action'] = update.message.text

    failed_orders = [order['name'] for order in tmp_data.failed_orders]

    update.message.reply_text(
        text='Список просроченных заказов',
        reply_markup=services.create_tg_keyboard_markup(failed_orders)
    )
    return EmployeeState.ORDERS


def get_order_info(update: Update, context: CallbackContext):
    action = context.user_data['action']
    if action == 'Список заказов':
        message_for_send = 'Вывожу информацию по активному заказу {}'.format(
            update.message.text
        )
    else:
        message_for_send = 'Вывожу информацию по неактивному заказу {}'.format(
            update.message.text
        )

    update.message.reply_text(
        message_for_send,
        reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def get_users_count_who_clicked_ad(update: Update, _):
    message_for_send = 'Количество пользователей прошедших по рекламе: 1'
    update.message.reply_text(
        message_for_send,
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
