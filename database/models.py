from datetime import datetime

from sqlalchemy import BigInteger, VARCHAR, ForeignKey
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship

BaseModel = declarative_base()  # Создание декларативной модели базы данных


class UserModel(BaseModel):
    """
    Модель данных для представления пользователей в базе данных.

    :ivar user_id: Уникальный ID пользователя в Telegram.
    :ivar username: Username пользователя в Telegram.
    :ivar first_name: Имя пользователя в Telegram.
    :ivar last_name: Фамилия пользователя в Telegram.
    :ivar name: Имя, указанное пользователем при регистрации в базе данных.
    :ivar department: Отделение, указанное пользователем при регистрации в базе данных.
    :ivar requests: Заявки пользователя, связанные с таблицей Requests.
    :ivar registration_time: Время регистрации пользователя.
    :type registration_time: datetime
    """
    __tablename__ = "Users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(VARCHAR(32), nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column()
    department: Mapped[str] = mapped_column()
    requests: Mapped[list["RequestModel"]] = relationship(back_populates="user", uselist=True, lazy="selectin")
    registration_time: Mapped[datetime] = mapped_column(default=datetime.now())


class RequestModel(BaseModel):
    """
    Модель данных для представления заявок пользователей в базе данных.

    :ivar request_id: Уникальный ID заявки пользователя.
    :ivar user: Пользователь, отправивший заявку, связанный с таблицей Users.
    :ivar user_fk: Внешний ключ в виде уникального ID для связи с пользователем.
    :ivar req_description: Описание заявки пользователя.
    :ivar photo_id: ID фотографии, прикрепленной к заявке (при ее наличии).
    :ivar video_id: ID видео, прикрепленного к заявке (при его наличии).
    :ivar status: Статус заявки пользователя ("В очереди"/"Выполняется"/"Выполнено").
    :ivar executor: ID исполнителя заявки пользователя.
    :ivar creation_time: Время создания заявки.
    :ivar completion_time: Время выполнения заявки.
    """
    __tablename__ = "Requests"

    request_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user: Mapped["UserModel"] = relationship(back_populates="requests", uselist=False)
    user_fk: Mapped[int] = mapped_column(ForeignKey("Users.user_id"))
    req_description: Mapped[str] = mapped_column()
    photo_id: Mapped[str] = mapped_column(default=None, nullable=True)
    video_id: Mapped[str] = mapped_column(default=None, nullable=True)
    status: Mapped[str] = mapped_column()
    executor: Mapped[int] = mapped_column(BigInteger, default=None, nullable=True)
    creation_time: Mapped[datetime] = mapped_column(default=datetime.now())
    completion_time: Mapped[datetime] = mapped_column(nullable=True)
