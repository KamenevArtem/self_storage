from telegram import Update
from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from telegram.ext import CallbackContext

from tg_bot import services

from tg_bot.models import Order, Customer
from tg_bot.states import EmployeeState


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
    kbd_layout = ['Заказ {}'.format(order.id) for order in orders]

    update.message.reply_text(
        text='Список активных заказов',
        reply_markup=services.create_tg_keyboard_markup(kbd_layout)
    )

    return EmployeeState.ORDERS


def get_failed_orders(update: Update, context: CallbackContext):
    context.user_data['action'] = update.message.text
    failed_orders = services.get_failed_orders_from_db()
    if not failed_orders:
        update.message.reply_text(
            'Нет просроченных заказов',
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    kbd_layout = ['Заказ {}'.format(order.id) for order in failed_orders]

    update.message.reply_text(
        text='Список просроченных заказов',
        reply_markup=services.create_tg_keyboard_markup(kbd_layout)
    )

    return EmployeeState.ORDERS


def get_order_info(update: Update, context: CallbackContext):
    action = context.user_data['action']
    order_id = update.message.text.split()[1]
    order = Order.objects.get(id=order_id)
    order_info = """
    Box: {}
    Срок хранения: {}
    Дата начала контракта: {}
    Дата доставки: {}
    Объём груза: {}
    Вес груза: {}
    Клиент: {}
    Подтверждение заказа: {}
    Выполнение заказа: {}
    """
    order_info_format = order_info.format(
        order.box,
        order.rent_time,
        order.order_start_date,
        order.delivery_time,
        order.cargo_size,
        order.cargo_weight,
        order.customer.name,
        'Нет' if order.conformation else 'Да',
        'Выполнен' if order.completed else 'Не выполнен'
    )
    if action == 'Список заказов':
        message_for_send = '  Информация по активному заказу {}'.format(
            order_info_format
        )
    else:
        message_for_send = '  Информация по просроченному заказу {}'.format(
            order_info_format
        )

    update.message.reply_text(
        message_for_send,
        reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def get_users_count_who_clicked_ad(update: Update, _):
    active_customers = Customer.objects.values_list('id').count()
    message_for_send = f'Количество активных пользователей {active_customers}'
    update.message.reply_text(
        message_for_send,
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
