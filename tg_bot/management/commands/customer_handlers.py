from telegram import Update
from telegram import ReplyKeyboardRemove
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler

from .keyboards import create_keyboard


START_CHOISE, LEAVE_CHOISE, DELIVERY_ORDER, WEIGHT_CHOISE, SIZE_CHOISE, ADRESS, PHONE_NUMBER, PRIVACY = range(8)


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Прошу прощения, данной команды я не знаю"
        )


def start(update: Update, context: CallbackContext):
    print(update.effective_chat.username)
    print(update.message.text)
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
        text='Хотели бы Вы оформить заказ?',
        reply_markup=create_keyboard(
            button_names, 
            buttons_per_row=2,
            need_start=True
            )
        )
    return LEAVE_CHOISE


def order_delivery(update: Update, context:CallbackContext):
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


def give_privacy_agreement(update: Update, context:CallbackContext):
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
    if update.message.text == 'Не знаю':
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Хорошо, мы замерим и сообщим точную цену при оформлении бокса',
            )
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


# def check_customer_information(update: Update, context:CallbackContext):
#     context.bot.send_message(
#             chat_id=update.effective_chat.id,
#             text='Верны ли Ваши данные?',
#             )
#     button_names= [
#         'Да',
#         'Нет'
#     ]
#     return CHECK


def take_staff(update: Update, context:CallbackContext):
    button_names= [
        'Заказ 1',
        'Заказ 2'
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


def print_FAQ(update: Update, context:CallbackContext):
    button_names= []
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Правила хранения нашего сервиса:',
        reply_markup=create_keyboard(
            button_names, 
            buttons_per_row=1,
            need_start=True
            )
        )


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
                get_customer_address,
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
                get_customer_address,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text,
                get_customer_address,
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
        ]
        
    },
    fallbacks=[
        CommandHandler('cancel', cancel),
        MessageHandler(Filters.text('отмена'), cancel)
    ]
)