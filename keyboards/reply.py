from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def cancel_change_userdata() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="Отменить изменение данных")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def cancel_create_request() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="Отменить создание заявки")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def cancel_registration() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="Отменить регистрацию")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def yes_no() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Да")
    keyboard.button(text="Нет")
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True, input_field_placeholder="Выберите кнопку")
