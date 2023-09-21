from aiogram import Router, F
from aiogram.filters import CommandStart, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot import keyboards as kb
from bot.states.register_state import RegisterState
from database import orm

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, sessionmaker: async_sessionmaker):
    """
    Функция для обработки команды /start.

    Функция получает данные пользователя из базы данных. Если пользователь зарегистрирован, то отправляет сообщение с
    приветствием, иначе устанавливает состояние RegisterState в name и предлагает пользователю зарегистрироваться,
    прикрепляя текстовую кнопку для отмены регистрации.

    :param message: Объект сообщения.
    :type message: Message
    :param state: Состояние с данными.
    :type state: FSMContext
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker
    """
    user = await orm.get_user(user_id=message.from_user.id,
                              sessionmaker=sessionmaker)
    if user is None:
        await state.set_state(state=RegisterState.name)
        await message.answer(text="Здравствуйте, Вас приветствует бот для принятия заявок в ЦМИТ.\n\n"
                                  "Похоже, вы открыли бота впервые. "
                                  "Для принятия заявок мне нужна некоторая информация о Вас.\n"
                                  "Как к Вам обращаться?",
                             reply_markup=kb.reply.cancel_registration())
    else:
        await message.answer(text=f"Добро пожаловать, {user.name}!\n\n"
                                  'Список доступных команд Вы можете посмотреть, нажав на кнопку "Меню" в нижнем левом '
                                  "углу или отправив команду /menu",
                             reply_markup=ReplyKeyboardRemove())


@router.message(or_f(*RegisterState.__states__), F.text.casefold() == "отменить регистрацию")
async def cancel_registration(message: Message, state: FSMContext):
    """
    Функция для отмены регистрации.

    Функция очищает состояние RegisterState и отправляет сообщение об отмене создания заявки с предложением
    зарегистрироваться позже.

    :param message: Объект сообщения.
    :type message: Message
    :param state: Состояние с данными.
    :type state: FSMContext
    """
    await state.clear()
    await message.answer(text="К сожалению, для получения доступа к функциональности бота, нужно пройти регистрацию.\n"
                              "Но мы всегда можем вернуться к этому позже. Просто отправьте команду /start для "
                              "возвращения к регистрации",
                         reply_markup=ReplyKeyboardRemove())


@router.message(RegisterState.name)
async def process_name(message: Message, state: FSMContext):
    """
    Функция для обработки состояния name из RegisterState.

    Функция добавляет текст сообщения в состояние RegisterState и устанавливает его в department. Затем отправляет
    сообщение с вопросом о кабинете пользователя, прикрепляя текстовую кнопку для отмены регистрации.

    :param message: Объект сообщения.
    :type message: Message
    :param state: Состояние с данными.
    :type state: FSMContext
    """
    if message.text is None:
        await message.reply(text="К сожалению, я не нашел текста в сообщении. Попробуйте еще раз.")
    else:
        await state.update_data(name=message.text)
        await state.set_state(state=RegisterState.department)
        await message.answer(text="Хорошо. Из какого Вы кабинета/отделения?",
                             reply_markup=kb.reply.cancel_registration())


@router.message(RegisterState.department)
async def process_department(message: Message, state: FSMContext):
    """
    Функция для обработки состояния department из RegisterState.

    Функция добавляет текст сообщения в состояние RegisterState и устанавливает его в confirm. Затем отправляет
    сообщение с внесенными данными для их подтверждения, прикрепляя соответствующие текстовые кнопки.

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
        await state.set_state(state=RegisterState.confirm)
        await message.answer(text="Отлично! Давайте проверим информацию.\n\n"
                                  f"Ваше имя: {data['name']}\n"
                                  f"Ваш кабинет/отделение: {message.text}\n\n"
                                  "Всё верно?",
                             reply_markup=kb.reply.yes_no())


@router.message(RegisterState.confirm, F.text.casefold() == "да")
async def process_confirm_yes(message: Message, state: FSMContext, sessionmaker: async_sessionmaker):
    """
    Функция для обработки состояния confirm из RegisterState при подтверждении пользователем.

    Функция забирает данные из состояния RegisterState и очищает его. Затем вносит данные пользователя в базу данных и
    оповещает его об успешности выполнения.

    :param message: Объект сообщения.
    :type message: Message
    :param state: Состояние с данными.
    :type state: FSMContext
    :param sessionmaker: Асинхронная фабрика для сессий.
    :type sessionmaker: async_sessionmaker
    """
    data = await state.get_data()
    await state.clear()
    await orm.add_user(user_id=message.from_user.id,
                       username=message.from_user.username,
                       first_name=message.from_user.first_name,
                       last_name=message.from_user.last_name,
                       name=data["name"],
                       department=data["department"],
                       sessionmaker=sessionmaker)
    await message.answer(text="Спасибо! Я запомнил.\n\n",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(text="Теперь Вы можете отправить команду /menu для отображения доступных команд")


@router.message(RegisterState.confirm, F.text.casefold() == "нет")
async def process_confirm_no(message: Message, state: FSMContext):
    """
     Функция для обработки состояния confirm из RegisterState при отклонении пользователем.

     Функция устанавливает состояние RegisterState в name и отправляет сообщение, предлагающее заново внести данные
     пользователя с прикрепленной текстовой кнопкой для отмены изменений.

     :param message: Объект сообщения.
     :type message: Message
     :param state: Состояние с данными.
     :type state: FSMContext
     """
    await state.set_state(state=RegisterState.name)
    await message.answer(text="Ничего страшного, начнем заново\n\n"
                              "Как к Вам обращаться?",
                         reply_markup=kb.reply.cancel_registration())


@router.message(RegisterState.confirm)
async def process_confirm(message: Message):
    """
    Функция для обработки состояния confirm из RegisterState.

    Функция отправляет сообщение о том, что нужно сделать выбор из текстовых кнопок "да" и "нет".

    :param message: Объект сообщения.
    :type message: Message
    """
    await message.answer(text='Извините, я не понял. Для подтверждения или отмены регистрации отправьте "да" или "нет"',
                         reply_markup=kb.reply.yes_no())
