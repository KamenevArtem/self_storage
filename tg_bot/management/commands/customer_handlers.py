import os
import qrcode

from telegram import Update
from telegram import ReplyKeyboardRemove
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler

from django.shortcuts import get_object_or_404
from tg_bot.models import Customer, Order
from .keyboards import create_keyboard


START_CHOISE, LEAVE_CHOISE, DELIVERY_ORDER, WEIGHT_CHOISE, SIZE_CHOISE, ADRESS, PHONE_NUMBER, PRIVACY, CHECK, MADE_ORDER, PRICE, TAKE_STAFF, SHOW_ORDERS, HANDLE_ORDER = range(14)


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
        )[0])
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
    order = customer.orders.last()
    order.cargo_size = update.message.text
    order.save()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Стоимость хранения будет составлять ... в месяц',
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


def give_privacy_agreement(update: Update, context:CallbackContext):
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
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Введите Ваш номер телефона',
        )
    return PHONE_NUMBER


def check_customer_information(update: Update, context:CallbackContext):
    button_names= [
        'Да',
        'Нет'
    ]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Верны ли Ваши данные?',
        reply_markup=create_keyboard(
            button_names, 
            buttons_per_row=2,
            )
        )
    return CHECK


def get_delivery_time(update: Update, context:CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Когда Вам удобно отправить груз?',
        )
    return MADE_ORDER


def create_order(update: Update, context:CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Спасибо за уделенное время. Доставщик заберет груз (дата/время), '
        'предварительно позвонив Вам. Для повторной сессии напишите в чат /start',
        )
    return ConversationHandler.END


def take_staff(update: Update, context:CallbackContext):
    button_names= [
        'Заказ 1',
        'Заказ 2',
    ]
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
    button_names= [
        'Забрать вещи',
        'Забрать вещи, но вернуть позже',
    ]
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
    if update.message.text == 'Забрать вещи, но вернуть позже':
        qr_content = [1,5,6,7,9,7,5]
        qr = qrcode.make(qr_content)
        qr.save('qr.png')
        with open('./qr.png', 'rb') as qr_code:
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=qr_code,
                )
    elif update.message.text == 'Забрать вещи':
        qr_content = [5,66666,778]
        qr = qrcode.make(qr_content)
        qr.save('qr.png')
        with open('./qr.png', 'rb') as qr_code:
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=qr_code,
                )
    else:
        return ConversationHandler.END
    os.remove('./qr.png')
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
            MessageHandler(
                Filters.text('Не знаю'),
                give_privacy_agreement,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text,
                show_price,
                pass_user_data=True,
            )
        ],
        PRICE: [
            MessageHandler(
                Filters.text('Да'),
                give_privacy_agreement,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Нет'),
                cancel,
                pass_user_data=True,
            )
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
            )
        ],
        ADRESS: [
            MessageHandler(
                Filters.text,
                get_phone_number,
                pass_user_data=True,
            )
        ],
        PHONE_NUMBER:[
            MessageHandler(
                Filters.text,
                check_customer_information,
                pass_user_data=True,
            )
        ],
        CHECK:[
            MessageHandler(
                Filters.text('Да'),
                get_delivery_time,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Нет'),
                get_customer_address,
                pass_user_data=True,
            )
        ],
        MADE_ORDER: [
            MessageHandler(
                Filters.text,
                create_order,
                pass_user_data=True,
            )
        ],
        SHOW_ORDERS: [
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
            MessageHandler(
                Filters.text('Стартовое меню'),
                start,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text,
                show_QR,
                pass_user_data=True,
            )
        ]
    },
    fallbacks=[
        CommandHandler('cancel', cancel),
        MessageHandler(Filters.text('отмена'), cancel)
    ]
)