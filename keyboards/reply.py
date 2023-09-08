from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def yes_no() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Да")
    keyboard.button(text="Нет")
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True, input_field_placeholder="Выберите кнопку")
