from aiogram import Router, F, Bot
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot import keyboards as kb
from bot.states import CreateRequestState
from bot.utils import answer_text, send_request
from database import orm

router = Router()


@router.message(Command("create_request"))
async def cmd_create_request(message: Message, state: FSMContext, sessionmaker: async_sessionmaker):
    """
    Функция для обработки команды /create_requests.

    Функция получает данные пользователя из базы данных, устанавливает состояние CreateRequestState в description и
    отправляет сообщение с предложением описать проблему, прикрепляя текстовую кнопку для отмены создания заявки.

    :param message: Объект сообщения.
    :type message: Message
    :param state: Состояние с данными.
    :type state: FSMContext
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker
    """
    user = await orm.get_user(user_id=message.from_user.id,
                              sessionmaker=sessionmaker)
    await state.set_state(state=CreateRequestState.description)
    await message.answer(text=f"Здравствуйте, {user.name}! Опишите Вашу проблему. "
                              "Вы также можете прислать фотографию или видео с подписью проблемы.",
                         reply_markup=kb.reply.cancel_create_request())


@router.message(or_f(*CreateRequestState.__states__), F.text.casefold() == "отменить создание заявки")
async def cancel_create_request(message: Message, state: FSMContext):
    """
    Функция для отмены создания заявки.

    Функция очищает состояние CreateRequestState и отправляет сообщение об отмене создания заявки.

    :param message: Объект сообщения.
    :type message: Message
    :param state: Состояние с данными.
    :type state: FSMContext
    """
    await state.clear()
    await message.answer("Создание заявки отменено",
                         reply_markup=ReplyKeyboardRemove())


@router.message(CreateRequestState.description)
async def process_description(message: Message, state: FSMContext, sessionmaker: async_sessionmaker):
    """
    Функция для обработки состояния description из CreateRequestState.

    Функция получает данные пользователя из базы данных, устанавливает состояние CreateRequestState в confirm, формирует
    текст заявки и отправляет его пользователю для подтверждения, прикрепляя соответствующие текстовые кнопки.

    :param message: Объект сообщения.
    :type message: Message
    :param state: Состояние с данными.
    :type state: FSMContext
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker
    """
    user = await orm.get_user(user_id=message.from_user.id,
                              sessionmaker=sessionmaker)
    await state.set_state(state=CreateRequestState.confirm)
    text = "Хорошо. Давайте сверим данные:\n\n"
    if message.photo:
        description = message.caption
        photo_id = message.photo[-1].file_id
        text += answer_text(request_id=None,
                            name=user.name,
                            department=user.department,
                            status=None,
                            description=description,
                            is_request_id=False,
                            is_status=False)
        text += "\n\nВсё верно?"
        await state.update_data(description=description, photo_id=photo_id, video_id=None)
        await message.answer_photo(photo=photo_id, caption=text, reply_markup=kb.reply.yes_no())
    elif message.video:
        description = message.caption
        video_id = message.video.file_id
        text += answer_text(request_id=None,
                            name=user.name,
                            department=user.department,
                            status=None,
                            description=description,
                            is_request_id=False,
                            is_status=False)
        text += "\n\nВсё верно?"
        await state.update_data(description=description, photo_id=None, video_id=video_id)
        await message.answer_video(video=video_id, caption=text, reply_markup=kb.reply.yes_no())
    else:
        text += answer_text(request_id=None,
                            name=user.name,
                            department=user.department,
                            status=None,
                            description=message.text,
                            is_request_id=False,
                            is_status=False)
        text += "\n\nВсё верно?"
        await state.update_data(description=message.text, photo_id=None, video_id=None)
        await message.answer(text=text, reply_markup=kb.reply.yes_no())


@router.message(CreateRequestState.confirm, F.text.casefold() == "да")
async def process_confirm_yes(message: Message, bot: Bot, state: FSMContext, sessionmaker: async_sessionmaker):
    """
    Функция для обработки состояния confirm из CreateRequestState при подтверждении пользователем.

    Функция забирает данные из состояния CreateRequestState и очищает его. Затем добавляет заявку в базу данных и
    оповещает пользователя об успешности выполнения. В конце отправляет заявку администраторам.

    :param message: Объект сообщения.
    :type message: Message
    :param bot: Объект бота.
    :type bot: Bot
    :param state: Состояние с данными.
    :type state: FSMContext
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker
    """
    data = await state.get_data()
    await state.clear()
    await orm.add_request(user_id=message.from_user.id,
                          req_description=data["description"],
                          photo_id=data["photo_id"],
                          video_id=data["video_id"],
                          sessionmaker=sessionmaker)
    requests = await orm.get_active_requests(user_id=message.from_user.id,
                                             sessionmaker=sessionmaker)
    await message.answer(text=f"Ваша заявка создана под номером <b>{requests[-1].request_id}</b>",
                         reply_markup=ReplyKeyboardRemove())
    await send_request(bot=bot,
                       user_id=message.from_user.id,
                       sessionmaker=sessionmaker)


@router.message(CreateRequestState.confirm, F.text.casefold() == "нет")
async def process_confirm_no(message: Message, state: FSMContext):
    """
    Функция для обработки состояния confirm из CreateRequestState при отклонении пользователем.

    Функция очищает состояние CreateRequestState и отправляет сообщение об отмене создания заявки.

    :param message: Объект сообщения.
    :type message: Message
    :param state: Состояние с данными.
    :type state: FSMContext
    """
    await state.clear()
    await message.answer(text="Создание заявки отменено",
                         reply_markup=ReplyKeyboardRemove())


@router.message(CreateRequestState.confirm)
async def process_confirm(message: Message):
    """
    Функция для обработки состояния confirm из CreateRequestState.

    Функция отправляет сообщение о том, что нужно сделать выбор из текстовых кнопок "да" и "нет".

    :param message: Объект сообщения.
    :type message: Message
    """
    await message.answer(text='Извините, я не понял. Для подтверждения или отмены изменений отправьте "да" или "нет"',
                         reply_markup=kb.reply.yes_no())
