from telegram.ext import Filters
from telegram.ext import ConversationHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler

from tg_bot.states import EmployeeState

from tg_bot.handlers import employee_handlers
from tg_bot.handlers import cancel


employee_conversation = ConversationHandler(
    entry_points=[
        CommandHandler(
            'start',
            employee_handlers.start_for_employer
        )
    ],
    states={
        EmployeeState.ACTION: [
            MessageHandler(
                Filters.text('Список заказов'),
                employee_handlers.get_all_orders,
                pass_user_data=True
            ),
            MessageHandler(
                Filters.text('Список просроченных заказов'),
                employee_handlers.get_failed_orders,
                pass_user_data=True
            ),
            MessageHandler(
                Filters.text('Пользователи пришедшие по рекламе'),
                employee_handlers.get_users_count_who_clicked_ad,
            )
        ],
        EmployeeState.ORDERS: [
            MessageHandler(
                Filters.text,
                employee_handlers.get_order_info,
            )
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel),
        MessageHandler(Filters.text('отмена'), cancel)
    ],
)
