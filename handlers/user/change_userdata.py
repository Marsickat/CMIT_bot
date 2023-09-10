from aiogram import Router, F
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

import keyboards as kb
from database import orm
from states import ChangeUserdataState

router = Router()


@router.message(Command("change_userdata"))
async def cmd_change_userdata(message: Message, state: FSMContext):
    await state.set_state(ChangeUserdataState.name)
    await message.answer("Давайте изменим данные. Как к Вам обращаться?",
                         reply_markup=kb.reply.cancel_change_userdata())


@router.message(or_f(*ChangeUserdataState.__states__), F.text.casefold() == "отменить изменение данных")
async def cancel_registration(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Изменения отменены",
                         reply_markup=ReplyKeyboardRemove())


@router.message(ChangeUserdataState.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ChangeUserdataState.department)
    await message.answer("Хорошо. Из какого Вы кабинета/отделения?",
                         reply_markup=kb.reply.cancel_change_userdata())


@router.message(ChangeUserdataState.department)
async def process_department(message: Message, state: FSMContext):
    await state.update_data(department=message.text)
    data = await state.get_data()
    await state.set_state(ChangeUserdataState.confirm)
    await message.answer("Отлично! Давайте проверим информацию.\n\n"
                         f"Ваше имя: {data['name']}\n"
                         f"Ваше подразделение: {message.text}\n\n"
                         "Всё верно?",
                         reply_markup=kb.reply.yes_no())


@router.message(ChangeUserdataState.confirm, F.text.casefold() == "да")
async def process_confirm_yes(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    await state.clear()
    await orm.change_userdata(message.from_user.id,
                              data["name"],
                              data["department"],
                              session)
    await message.answer("Спасибо! Я запомнил.",
                         reply_markup=ReplyKeyboardRemove())


@router.message(ChangeUserdataState.confirm, F.text.casefold() == "нет")
async def process_confirm_no(message: Message, state: FSMContext):
    await state.set_state(ChangeUserdataState.name)
    await message.answer("Ничего страшного, начнем заново\n\n"
                         "Как к Вам обращаться?",
                         reply_markup=kb.reply.cancel_change_userdata())


@router.message(ChangeUserdataState.confirm)
async def process_confirm(message: Message):
    await message.answer('Извините, я не понял. Для подтверждения или отмены изменений отправьте "да" или "нет"',
                         reply_markup=kb.reply.yes_no())
