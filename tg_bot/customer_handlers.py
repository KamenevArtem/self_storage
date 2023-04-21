import datetime
import os
import qrcode
import phonenumbers

from telegram import Update
from telegram import ReplyKeyboardRemove
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler

from django.utils import timezone
from tg_bot.models import Customer, Order, Box
from .keyboards import create_keyboard


START_CHOISE, LEAVE_CHOISE, DELIVERY_ORDER, WEIGHT_CHOISE, SIZE_CHOISE, ADRESS, PHONE_NUMBER, PRIVACY, CHECK, MADE_ORDER, PRICE, TAKE_STAFF, SHOW_ORDERS, HANDLE_ORDER, RENT = range(15)


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Прошу прощения, данной команды я не знаю"
        )


def start(update: Update, context: CallbackContext):
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
        reply_markup=create_keyboard(
            button_names, 
            buttons_per_row=3,
            need_start=False
            )
        )
    return START_CHOISE


def leave_staff(update: Update, context:CallbackContext):
    button_names = [
        'Оформить заказ'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Рады, что Вы выбираете нас! Хотели бы оформить заказ?',
        reply_markup=create_keyboard(
            button_names, 
            buttons_per_row=2,
            need_start=True
            )
        )
    return LEAVE_CHOISE


def order_delivery(update: Update, context:CallbackContext):
    Order.objects.create(
        customer=Customer.objects.filter(
        external_id=update.effective_chat.id
        )[0]
        )
    button_names = [
        'Заказать бесплатную доставку',
        'Привезу сам'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Вам необходима помощь курьера?',
        reply_markup=create_keyboard(
            button_names, 
            buttons_per_row=3,
            need_start=True
            )
        )
    return DELIVERY_ORDER


def get_staff_weight(update: Update, context:CallbackContext):
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
        reply_markup=create_keyboard(
            button_names, 
            buttons_per_row=3,
            )
        )
    return WEIGHT_CHOISE


def get_staff_size(update: Update, context:CallbackContext):
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
        reply_markup=create_keyboard(
            button_names, 
            buttons_per_row=3,
            )
        )
    return SIZE_CHOISE


def show_price(update: Update, context:CallbackContext):
    customer = Customer.objects.get(name=update.effective_chat.username)
    box = Box.objects.get(size=update.message.text)
    rent_price_per_month = box.rental_price*30
    order = customer.orders.last()
    order.cargo_size = update.message.text
    order.box = box
    order.save()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Стоимость хранения будет составлять {rent_price_per_month} рублей в месяц',
        )
    button_names = [
        'Да',
        'Нет'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Вас устраивает текущая стоимость?',
        reply_markup=create_keyboard(
            button_names, 
            buttons_per_row=2,
            )
        )
    return PRICE


def get_rent_time(update: Update, context:CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='На сколько дней Вы хотите оставить вещи?')
    return RENT


def give_privacy_agreement(update: Update, context:CallbackContext):
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
        reply_markup=create_keyboard(
            button_names, 
            buttons_per_row=2,
            )
        )
    return PRIVACY


def get_customer_address(update: Update, context:CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Введите Ваш адрес',
        )
    return ADRESS


def get_phone_number(update: Update, context:CallbackContext):
    customer = Customer.objects.get(name=update.effective_chat.username)
    customer.address = update.message.text
    customer.save()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Введите Ваш номер телефона',
        )
    return PHONE_NUMBER


def check_customer_information(update: Update, context:CallbackContext):
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
        return PHONE_NUMBER
    if phonenumbers.is_valid_number(parsed_phonenumber):
        customer.phone_number = phonenumbers.format_number(
            parsed_phonenumber,
            phonenumbers.PhoneNumberFormat.E164
            )
        customer.save()
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Введеный Вами номер телефона не существует. Попробуйте ввести через +7',
        )
        return PHONE_NUMBER
    button_names= [
        'Да',
        'Нет'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Верны ли Ваши данные?\n Адрес: {customer.address} '
             f'Номер телефона: {update.message.text}',
        reply_markup=create_keyboard(
            button_names, 
            buttons_per_row=2,
            )
        )
    return CHECK


def get_delivery_time(update: Update, context:CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='В какой день Вам удобно отправить вещи?'
             'Введите дату в формате: год-месяц-день',
        )
    return MADE_ORDER


def create_order(update: Update, context:CallbackContext):
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
        return MADE_ORDER
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Спасибо за уделенное время. Доставщик заберет вещи {order.delivery_time}, '
             f'предварительно позвонив Вам. Для повторной сессии напишите в чат /start',
        )
    return ConversationHandler.END


def take_staff(update: Update, context:CallbackContext):
    customer = Customer.objects.get(name=update.effective_chat.username)
    orders = customer.orders.all()
    button_names = [f'Заказ {number}' for number, order in enumerate(orders, start=1)]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Какой заказ Вас интересует?',
        reply_markup=create_keyboard(
            button_names, 
            buttons_per_row=3,
            need_start=True
            )
        )
    return SHOW_ORDERS


def show_orders(update: Update, context:CallbackContext):
    customer = Customer.objects.get(name=update.effective_chat.username)
    orders = customer.orders.all()
    order = orders.get(id=update.message.text.split(' ')[1])
    button_names= [
        f'Забрать вещи. Заказ {order.id}',
        f'Забрать вещи, но вернуть позже.',
    ]
    close_qr_content = {
        'Номер заказа' : order.id,
        'Время хранения' : order.rent_time,
        'Время истечения срока хранения' : order.order_end_date,
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
        reply_markup=create_keyboard(
            button_names, 
            buttons_per_row=3,
            need_start=True
            )
        )
    return HANDLE_ORDER


def show_QR(update: Update, context:CallbackContext):
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


def print_FAQ(update: Update, context:CallbackContext):
    button_names= []
    button_names = [
        'Оставить вещи',
        'Забрать вещи',
        'Узнать правила хранения'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Правила хранения нашего сервиса:',
        reply_markup=create_keyboard(
            button_names, 
            buttons_per_row=3,
            need_start=False
            )
        )
    return START_CHOISE


def cancel(update, _):
    update.message.reply_text(
        'Спасибо за уделенное Вами время',
        reply_markup=ReplyKeyboardRemove()
        )
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler(
            'start',
            start
        ),
        MessageHandler(
            Filters.text('Стартовое меню'),
            start
        )
    ],
    states={
        START_CHOISE: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Оставить вещи'),
                leave_staff,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Забрать вещи'),
                take_staff,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Узнать правила хранения'),
                print_FAQ,
                pass_user_data=True,
            )
        ],
        LEAVE_CHOISE: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Оформить заказ'),
                order_delivery,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Стартовое меню'),
                start,
                pass_user_data=True,
            ),
        ],
        DELIVERY_ORDER: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Заказать бесплатную доставку'),
                get_staff_weight,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Привезу сам'),
                get_staff_weight,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Стартовое меню'),
                start,
                pass_user_data=True,
            )
        ],
        WEIGHT_CHOISE: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Не знаю'),
                give_privacy_agreement,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text,
                get_staff_size,
                pass_user_data=True,
            ),
        ],
        SIZE_CHOISE: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Не знаю'),
                give_privacy_agreement,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text,
                show_price,
                pass_user_data=True,
            ),
        ],
        PRICE: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Да'),
                get_rent_time,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Нет'),
                cancel,
                pass_user_data=True,
            ),
        ],
        RENT: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text,
                give_privacy_agreement,
                pass_user_data=True,
            ),
        ],
        PRIVACY: [
            MessageHandler(
                Filters.text('Согласен'),
                get_customer_address,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Не согласен'),
                start,
                pass_user_data=True,
            ),
            CommandHandler('cancel', cancel),
        ],
        ADRESS: [
            MessageHandler(
                Filters.text,
                get_phone_number,
                pass_user_data=True,
            ),
            CommandHandler('cancel', cancel),
        ],
        PHONE_NUMBER:[
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text,
                check_customer_information,
                pass_user_data=True,
            ),
        ],
        CHECK:[
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Да'),
                get_delivery_time,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Нет'),
                get_customer_address,
                pass_user_data=True,
            ),
        ],
        MADE_ORDER: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text,
                create_order,
                pass_user_data=True,
            ),
        ],
        SHOW_ORDERS: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Стартовое меню'),
                start,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text,
                show_orders,
                pass_user_data=True,
            ),
        ],
        HANDLE_ORDER: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Стартовое меню'),
                start,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text,
                show_QR,
                pass_user_data=True,
            ),
        ]
    },
    fallbacks=[
        CommandHandler('cancel', cancel),
        MessageHandler(Filters.text('отмена'), cancel)
    ]
)