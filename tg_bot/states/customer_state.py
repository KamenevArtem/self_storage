from enum import IntEnum


class CustomerState(IntEnum):
    START_CHOICE = 1
    LEAVE_CHOICE = 2
    DELIVERY_ORDER = 3
    WEIGHT_CHOICE = 4
    SIZE_CHOICE = 5
    ADDRESS = 6
    PHONE_NUMBER = 7
    PRIVACY = 8
    CHECK = 9
    MADE_ORDER = 10
    PRICE = 11
    TAKE_STAFF = 12
    SHOW_ORDERS = 13
    HANDLE_ORDER = 14
    RENT = 15
