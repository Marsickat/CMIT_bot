from datetime import datetime

from sqlalchemy import BigInteger, VARCHAR, ForeignKey
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship

BaseModel = declarative_base()


class UserModel(BaseModel):
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
