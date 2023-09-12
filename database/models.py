from datetime import datetime

from sqlalchemy import BigInteger, VARCHAR, ForeignKey
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship

BaseModel = declarative_base()  # Создание декларативной модели базы данных


class UserModel(BaseModel):
    """
    Модель данных для представления пользователей в базе данных.

    :param user_id: Уникальный ID пользователя в Telegram.
    :type user_id: int
    :param username: Username пользователя в Telegram.
    :type username: str
    :param first_name: Имя пользователя в Telegram.
    :type first_name: str
    :param last_name: Фамилия пользователя в Telegram.
    :type last_name: str
    :param name: Имя, указанное пользователем при регистрации в базе данных.
    :type name: str
    :param department: Отделение, указанное пользователем при регистрации в базе данных.
    :type department: str
    :param requests: Заявки пользователя, связанные с таблицей Requests.
    :type requests: list["RequestModel"]
    :param registration_time: Время регистрации пользователя.
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

    :param request_id: Уникальный ID заявки пользователя.
    :type request_id: int
    :param user: Пользователь, отправивший заявку, связанный с таблицей Users.
    :type user: UserModel
    :param user_fk: Внешний ключ в виде уникального ID для связи с пользователем.
    :type user_fk: int
    :param req_description: Описание заявки пользователя.
    :type req_description: str
    :param photo_id: ID фотографии, прикрепленной к заявке (при ее наличии).
    :type photo_id: str
    :param video_id: ID видео, прикрепленного к заявке (при его наличии).
    :type video_id: str
    :param status: Статус заявки пользователя ("В очереди"/"Выполняется"/"Выполнено").
    :type status: str
    :param creation_time: Время создания заявки.
    :type creation_time: datetime
    :param completion_time: Время выполнения заявки.
    :type completion_time: datetime
    """
    __tablename__ = "Requests"

    request_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    user: Mapped["UserModel"] = relationship(back_populates="requests", uselist=False)
    user_fk: Mapped[int] = mapped_column(ForeignKey("Users.user_id"))
    req_description: Mapped[str] = mapped_column()
    photo_id: Mapped[str] = mapped_column(default=None, nullable=True)
    video_id: Mapped[str] = mapped_column(default=None, nullable=True)
    status: Mapped[str] = mapped_column()
    creation_time: Mapped[datetime] = mapped_column(default=datetime.now())
    completion_time: Mapped[datetime] = mapped_column(nullable=True)
