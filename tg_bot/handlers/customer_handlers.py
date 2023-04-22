import datetime
import os

import phonenumbers
import qrcode

from telegram import Update

from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler

from tg_bot import services
from tg_bot.states import CustomerState
from tg_bot.models import Customer, Order, Box


def start_for_customer(update: Update, context: CallbackContext):
    Customer.objects.update_or_create(
        external_id=update.effective_chat.id,
        name=update.effective_chat.username
    )
    button_names = [
        'Оставить вещи',
        'Забрать вещи',
        'Узнать правила хранения'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Что Вас интересует?',
        reply_markup=services.create_tg_keyboard_markup(
            button_names,
            buttons_per_row=3,
            need_start=False
        )
    )
    return CustomerState.START_CHOICE


def leave_staff(update: Update, context: CallbackContext):
    button_names = [
        'Оформить заказ'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Рады, что Вы выбираете нас! Хотели бы оформить заказ?',
        reply_markup=services.create_tg_keyboard_markup(
            button_names,
            buttons_per_row=2,
            need_start=True
        )
    )
    return CustomerState.LEAVE_CHOICE


def order_delivery(update: Update, context: CallbackContext):
    Order.objects.create(
        customer=Customer.objects.filter(
            external_id=update.effective_chat.id
        )[0])
    button_names = [
        'Заказать бесплатную доставку',
        'Привезу сам'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Вам необходима помощь курьера?',
        reply_markup=services.create_tg_keyboard_markup(
            button_names,
            buttons_per_row=3,
            need_start=True
        )
    )
    return CustomerState.DELIVERY_ORDER


def get_staff_weight(update: Update, context: CallbackContext):
    if update.message.text == 'Привезу сам':
        customer = Customer.objects.get(name=update.effective_chat.username)
        order = customer.orders.last()
        order.need_delivery = 'Нет'
        order.save()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Адрес нашего склада:',
        )
    button_names = [
        'До 10 кг',
        '10-25 кг',
        '25-40 кг',
        '40-70 кг',
        '70-100 кг',
        'Более 100 кг',
        'Не знаю'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Какой вес Ваших вещей?',
        reply_markup=services.create_tg_keyboard_markup(
            button_names,
            buttons_per_row=3,
        )
    )
    return CustomerState.WEIGHT_CHOICE


def get_staff_size(update: Update, context: CallbackContext):
    customer = Customer.objects.get(name=update.effective_chat.username)
    order = customer.orders.last()
    order.cargo_weight = update.message.text
    order.save()
    button_names = [
        'Менее 3 кв.м',
        '3-7 кв.м',
        '7-10 кв.м',
        'Более 10 кв.м',
        'Не знаю'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Какой объём бокса Вам необходим?',
        reply_markup=services.create_tg_keyboard_markup(
            button_names,
            buttons_per_row=3,
        )
    )
    return CustomerState.SIZE_CHOICE


def show_price(update: Update, context: CallbackContext):
    customer = Customer.objects.get(name=update.effective_chat.username)
    box = Box.objects.get(size=update.message.text)
    rent_price_per_month = box.rental_price * 30
    order = customer.orders.last()
    order.cargo_size = update.message.text
    order.box = box
    order.save()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Стоимость хранения будет составлять {} рублей в месяц'.format(
            rent_price_per_month
        ),
    )
    button_names = [
        'Да',
        'Нет'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Вас устраивает текущая стоимость?',
        reply_markup=services.create_tg_keyboard_markup(
            button_names,
            buttons_per_row=2,
        )
    )
    return CustomerState.PRICE


def get_rent_time(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='На сколько дней Вы хотите оставить вещи?')
    return CustomerState.RENT


def give_privacy_agreement(update: Update, context: CallbackContext):
    customer = Customer.objects.get(name=update.effective_chat.username)
    order = customer.orders.last()
    order.rent_time = update.message.text
    order.save()

    if update.message.text == 'Не знаю':
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Хорошо, мы замерим и сообщим точную цену при оформлении бокса',
        )
    button_names = [
        'Согласен',
        'Не согласен'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Пользовательское соглашение:',
        reply_markup=services.create_tg_keyboard_markup(
            button_names,
            buttons_per_row=2,
        )
    )
    return CustomerState.PRIVACY


# TODO убрать если не используется больше
def get_customer_address(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Введите Ваш адрес',
    )
    return CustomerState.ADDRESS


def get_phone_number(update: Update, context: CallbackContext):
    customer = Customer.objects.get(name=update.effective_chat.username)
    customer.address = update.message.text
    customer.save()

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Введите Ваш номер телефона',
    )
    return CustomerState.PHONE_NUMBER


# TODO посмотреть, мне кажется слишком сложная логика =)
def check_customer_information(update: Update, context: CallbackContext):
    customer = Customer.objects.get(
        external_id=update.effective_chat.id,
    )
    try:
        parsed_phonenumber = phonenumbers.parse(
            update.message.text,
            'RU'
        )
    except:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Номер телефона был введен неправильно, повторите попытку',
        )
        return CustomerState.PHONE_NUMBER

    if phonenumbers.is_valid_number(parsed_phonenumber):
        customer.phone_number = phonenumbers.format_number(
            parsed_phonenumber,
            phonenumbers.PhoneNumberFormat.E164
        )
        customer.save()
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Введеный Вами номер телефона не существует. Попробуйте '
                 'ввести через +7',
        )
        return CustomerState.PHONE_NUMBER
    button_names = [
        'Да',
        'Нет'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Верны ли Ваши данные?\n Адрес: {customer.address} '
             f'Номер телефона: {update.message.text}',
        reply_markup=services.create_tg_keyboard_markup(
            button_names,
            buttons_per_row=2,
        )
    )
    return CustomerState.CHECK


def get_delivery_time(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='В какой день Вам удобно отправить вещи?'
             'Введите дату в формате: год-месяц-день',
    )
    return CustomerState.MADE_ORDER


def create_order(update: Update, context: CallbackContext):
    customer = Customer.objects.get(name=update.effective_chat.username)
    order = customer.orders.last()
    order.conformation = True
    order.save()
    try:
        delivery_time = datetime.datetime.strptime(
            update.message.text,
            '%Y-%m-%d').date()
        order.delivery_time = delivery_time
        order.order_end_date = order.delivery_time + datetime.timedelta(
            days=order.rent_time
        )
        order.save()
    except:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Попробуйте ещё раз, например 2023-06-15',
        )
        return CustomerState.MADE_ORDER
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Спасибо за уделенное время. Доставщик заберет вещи {order.delivery_time}, '
             f'предварительно позвонив Вам. Для повторной сессии напишите в чат /start',
    )
    return ConversationHandler.END


def take_staff(update: Update, context: CallbackContext):
    customer = Customer.objects.get(name=update.effective_chat.username)
    orders = customer.orders.all()
    button_names = [f'Заказ {number}' for number, order in
                    enumerate(orders, start=1)]

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Какой заказ Вас интересует?',
        reply_markup=services.create_tg_keyboard_markup(
            button_names,
            buttons_per_row=3,
            need_start=True
        )
    )
    return CustomerState.SHOW_ORDERS


def show_orders(update: Update, context: CallbackContext):
    customer = Customer.objects.get(name=update.effective_chat.username)
    orders = customer.orders.all()
    order = orders.get(id=update.message.text.split(' ')[1])
    button_names = [
        f'Забрать вещи. Заказ {order.id}',
        f'Забрать вещи, но вернуть позже.',
    ]
    close_qr_content = {
        'Номер заказа': order.id,
        'Время хранения': order.rent_time,
        'Время истечения срока хранения': order.order_end_date,
        'Статус заказа': 'Заказ закрыт'
    }
    close_qr = qrcode.make(close_qr_content)
    close_qr.save('cl_qr.png')
    back_qr_content = {
        'Номер заказа': order.id,
        'Время хранения': order.rent_time,
        'Время истечения срока хранения': order.order_end_date,
        'Статус заказа': 'Заказ приостановлен'
    }
    back_qr = qrcode.make(back_qr_content)
    back_qr.save('b_qr.png')
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Что Вас интересует?',
        reply_markup=services.create_tg_keyboard_markup(
            button_names,
            buttons_per_row=3,
            need_start=True
        )
    )
    return CustomerState.HANDLE_ORDER


def show_QR(update: Update, context: CallbackContext):
    customer = Customer.objects.get(name=update.effective_chat.username)
    orders = customer.orders.all()
    order_id = update.message.text.split(' ')[-1]
    order = orders.get(id=order_id)
    if update.message.text == 'Забрать вещи, но вернуть позже':
        with open('./b_qr.png', 'rb') as qr_code:
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=qr_code,
            )
    else:
        with open('./cl_qr.png', 'rb') as qr_code:
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=qr_code,
            )
            order.completed = True
            order.save()
    os.remove('./cl_qr.png')
    os.remove('./b_qr.png')
    return ConversationHandler.END


def print_FAQ(update: Update, context: CallbackContext):
    button_names = [
        'Оставить вещи',
        'Забрать вещи',
        'Узнать правила хранения'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Правила хранения нашего сервиса:',
        reply_markup=services.create_tg_keyboard_markup(
            button_names,
            buttons_per_row=3,
            need_start=False
        )
    )
    return CustomerState.START_CHOICE
