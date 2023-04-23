from telegram.ext import ConversationHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from tg_bot.states import CustomerState
from tg_bot.handlers import customer_handlers
from tg_bot.handlers import cancel


customer_conversation = ConversationHandler(
    entry_points=[
        CommandHandler(
            'start',
            customer_handlers.start_for_customer
        ),
        MessageHandler(
            Filters.text('Стартовое меню'),
            customer_handlers.start_for_customer
        )
    ],
    states={
        CustomerState.START_CHOICE: [
            MessageHandler(
                Filters.text('Оставить вещи'),
                customer_handlers.leave_staff,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Забрать вещи'),
                customer_handlers.take_staff,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Узнать правила хранения'),
                customer_handlers.print_FAQ,
                pass_user_data=True,
            )
        ],
        CustomerState.LEAVE_CHOICE: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Оформить заказ'),
                customer_handlers.order_delivery,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Стартовое меню'),
                customer_handlers.start_for_customer,
                pass_user_data=True,
            ),
        ],
        CustomerState.DELIVERY_ORDER: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Заказать бесплатную доставку'),
                customer_handlers.get_staff_weight,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Привезу сам'),
                customer_handlers.get_staff_weight,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Стартовое меню'),
                customer_handlers.start_for_customer,
                pass_user_data=True,
            )
        ],
        CustomerState.WEIGHT_CHOICE: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Не знаю'),
                customer_handlers.give_privacy_agreement,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text,
                customer_handlers.get_staff_size,
                pass_user_data=True,
            ),
        ],
        CustomerState.SIZE_CHOICE: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Не знаю'),
                customer_handlers.give_privacy_agreement,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text,
                customer_handlers.show_price,
                pass_user_data=True,
            )
        ],
        CustomerState.PRICE: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Да'),
                customer_handlers.get_rent_time,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Нет'),
                cancel,
                pass_user_data=True,
            )
        ],
        CustomerState.RENT: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text,
                customer_handlers.give_privacy_agreement,
                pass_user_data=True,
            ),
        ],
        CustomerState.PRIVACY: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Согласен'),
                customer_handlers.get_customer_address,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Не согласен'),
                customer_handlers.start_for_customer,
                pass_user_data=True,
            )
        ],
        CustomerState.ADDRESS: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text,
                customer_handlers.get_phone_number,
                pass_user_data=True,
            )
        ],
        CustomerState.PHONE_NUMBER: [
            MessageHandler(
                Filters.text,
                customer_handlers.check_customer_information,
                pass_user_data=True,
            )
        ],
        CustomerState.CHECK: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Да'),
                customer_handlers.get_delivery_time,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text('Нет'),
                customer_handlers.get_customer_address,
                pass_user_data=True,
            )
        ],
        CustomerState.MADE_ORDER: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text,
                customer_handlers.create_order,
                pass_user_data=True,
            )
        ],
        CustomerState.SHOW_ORDERS: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Стартовое меню'),
                customer_handlers.start_for_customer,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text,
                customer_handlers.show_orders,
                pass_user_data=True,
            ),
        ],
        CustomerState.HANDLE_ORDER: [
            CommandHandler('cancel', cancel),
            MessageHandler(
                Filters.text('Стартовое меню'),
                customer_handlers.start_for_customer,
                pass_user_data=True,
            ),
            MessageHandler(
                Filters.text,
                customer_handlers.show_QR,
                pass_user_data=True,
            )
        ]
    },
    fallbacks=[
        CommandHandler('cancel', cancel),
        MessageHandler(Filters.text('отмена'), cancel)
    ]
)
