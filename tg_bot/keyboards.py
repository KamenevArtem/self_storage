from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup


def create_keyboard(
    button_names,
    buttons_per_row=3,
    need_start=False
) -> ReplyKeyboardMarkup:
    button_names = [KeyboardButton(text) for text in button_names]
    rows = [
        button_names[number:number + buttons_per_row] for number in
        range(0, len(button_names), buttons_per_row)
    ]
    if need_start:
        rows.append([KeyboardButton('Стартовое меню')])
    return ReplyKeyboardMarkup(
        rows,
        resize_keyboard=True,
        one_time_keyboard=True
    )