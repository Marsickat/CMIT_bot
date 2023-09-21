from aiogram import Router, F
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot import keyboards as kb
from database import orm
from bot.states import ChangeUserdataState

router = Router()


@router.message(Command("change_userdata"))
async def cmd_change_userdata(message: Message, state: FSMContext):
    """
    Функция для обработки команды /change_userdata.

    Функция устанавливает состояние ChangeUserdataState в name и отправляет сообщение, предлагающее изменить данные
    пользователя с прикрепленной текстовой кнопкой для отмены изменений.

    :param message: Объект сообщения.
    :type message: Message
    :param state: Состояние с данными.
    :type state: FSMContext
    """
    await state.set_state(state=ChangeUserdataState.name)
    await message.answer(text="Давайте изменим данные. Как к Вам обращаться?",
                         reply_markup=kb.reply.cancel_change_userdata())


@router.message(or_f(*ChangeUserdataState.__states__), F.text.casefold() == "отменить изменение данных")
async def cancel_registration(message: Message, state: FSMContext):
    """
    Функция для отмены изменений данных пользователя.

    Функция очищает состояние ChangeUserdataState и отправляет сообщение об отмене изменения данных пользователя.

    :param message: Объект сообщения.
    :type message: Message
    :param state: Состояние с данными.
    :type state: FSMContext
    """
    await state.clear()
    await message.answer(text="Изменения отменены",
                         reply_markup=ReplyKeyboardRemove())


@router.message(ChangeUserdataState.name)
async def process_name(message: Message, state: FSMContext):
    """
    Функция для обработки состояния name из ChangeUserdataState.

    Функция добавляет текст сообщения в состояние ChangeUserdataState и устанавливает его в department. Затем отправляет
    вопрос про отделение, прикрепляя текстовую кнопку для отмены изменений.

    :param message: Объект сообщения.
    :type message: Message
    :param state: Состояние с данными.
    :type state: FSMContext
    """
    if message.text is None:
        await message.reply(text="К сожалению, я не нашел текста в сообщении. Попробуйте еще раз.")
    else:
        await state.update_data(name=message.text)
        await state.set_state(state=ChangeUserdataState.department)
        await message.answer(text="Хорошо. Из какого Вы кабинета/отделения?",
                             reply_markup=kb.reply.cancel_change_userdata())


@router.message(ChangeUserdataState.department)
async def process_department(message: Message, state: FSMContext):
    """
    Функция для обработки состояния department из ChangeUserdataState.

    Функция добавляет текст сообщения в состояние ChangeUserdataState и устанавливает его в confirm. Затем отправляет
    сообщение с измененными данными для их подтверждения, прикрепляя соответствующие текстовые кнопки.

    :param message: Объект сообщения.
    :type message: Message
    :param state: Состояние с данными.
    :type state: FSMContext
    """
    if message.text is None:
        await message.reply(text="К сожалению, я не нашел текста в сообщении. Попробуйте еще раз.")
    else:
        await state.update_data(department=message.text)
        data = await state.get_data()
        await state.set_state(state=ChangeUserdataState.confirm)
        await message.answer(text="Отлично! Давайте проверим информацию.\n\n"
                                  f"Ваше имя: {data['name']}\n"
                                  f"Ваше подразделение: {message.text}\n\n"
                                  "Всё верно?",
                             reply_markup=kb.reply.yes_no())


@router.message(ChangeUserdataState.confirm, F.text.casefold() == "да")
async def process_confirm_yes(message: Message, state: FSMContext, sessionmaker: async_sessionmaker):
    """
    Функция для обработки состояния confirm из ChangeUserdataState при подтверждении пользователем.

    Функция забирает данные из состояния ChangeUserdataState и очищает его. Затем вносит изменения в базу данных и
    оповещает пользователя об успешности выполнения.

    :param message: Объект сообщения.
    :type message: Message
    :param state: Состояние с данными.
    :type state: FSMContext
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker
    """
    data = await state.get_data()
    await state.clear()
    await orm.change_userdata(user_id=message.from_user.id,
                              name=data["name"],
                              department=data["department"],
                              sessionmaker=sessionmaker)
    await message.answer(text="Спасибо! Я запомнил.",
                         reply_markup=ReplyKeyboardRemove())


@router.message(ChangeUserdataState.confirm, F.text.casefold() == "нет")
async def process_confirm_no(message: Message, state: FSMContext):
    """
    Функция для обработки состояния confirm из ChangeUserdataState при отклонении пользователем.

    Функция устанавливает состояние ChangeUserdataState в name и отправляет сообщение, предлагающее заново изменить
    данные пользователя с прикрепленной текстовой кнопкой для отмены изменений.

    :param message: Объект сообщения.
    :type message: Message
    :param state: Состояние с данными.
    :type state: FSMContext
    """
    await state.set_state(state=ChangeUserdataState.name)
    await message.answer(text="Ничего страшного, начнем заново\n\n"
                              "Как к Вам обращаться?",
                         reply_markup=kb.reply.cancel_change_userdata())


@router.message(ChangeUserdataState.confirm)
async def process_confirm(message: Message):
    """
    Функция для обработки состояния confirm из ChangeUserdataState.

    Функция отправляет сообщение о том, что нужно сделать выбор из текстовых кнопок "да" и "нет".

    :param message: Объект сообщения.
    :type message: Message
    """
    await message.answer(text='Извините, я не понял. Для подтверждения или отмены изменений отправьте "да" или "нет"',
                         reply_markup=kb.reply.yes_no())
