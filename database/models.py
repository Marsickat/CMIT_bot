from datetime import datetime

from sqlalchemy import BigInteger, VARCHAR
from sqlalchemy.orm import declarative_base, mapped_column, Mapped

BaseModel = declarative_base()


class UserModel(BaseModel):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(VARCHAR(32), nullable=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column()
    department: Mapped[str] = mapped_column()
    registration_time: Mapped[datetime] = mapped_column(default=datetime.now())
