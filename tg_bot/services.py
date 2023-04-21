from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup


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
