import datetime

from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from tg_bot.models import Order


def create_tg_keyboard_markup(
        buttons_text: list,
        buttons_per_row: int = 3,
        need_start: bool = False
) -> ReplyKeyboardMarkup:
    keyboard_buttons = [KeyboardButton(text) for text in buttons_text]

    rows = [
        keyboard_buttons[i:i + buttons_per_row] for i in
        range(0, len(keyboard_buttons), buttons_per_row)
    ]
    if need_start:
        rows.append([KeyboardButton('Стартовое меню')])

    return ReplyKeyboardMarkup(
        rows,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_finish_rent_time(order: Order) -> datetime:
    finish_rent_time = order.order_start_date + datetime.timedelta(
        days=order.rent_time
    )
    return finish_rent_time


def get_failed_orders_from_db() -> list[Order] | None:
    non_closed_orders = Order.objects.filter(
        completed=False,
        rent_time__isnull=False
    )

    if not non_closed_orders:
        return

    current_date = datetime.datetime.now().date()
    failed_orders = []
    for order in non_closed_orders:
        if current_date > get_finish_rent_time(order):
            if not order.completed:
                failed_orders.append(order)

    if failed_orders:
        return failed_orders
