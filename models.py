from config import settings
from dotenv import load_dotenv, find_dotenv
from os import getenv
from sqlalchemy import String, create_engine
from sqlalchemy import BIGINT
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"


class PomodoroUser(Base):
    user_id: Mapped[int] = mapped_column(BIGINT)


class User(Base):
    user_id: Mapped[int] = mapped_column(BIGINT)
    datetime: Mapped[str] = mapped_column()


class Train(Base):
    user_id: Mapped[int] = mapped_column(BIGINT)
    answers: Mapped[str] = mapped_column()


class InfoTraining(Base):
    user_id: Mapped[int] = mapped_column(BIGINT)
    answers: Mapped[str] = mapped_column()


class ReflectAnswers(Base):
    user_id: Mapped[int] = mapped_column(BIGINT)
    answers: Mapped[str] = mapped_column()

load_dotenv(find_dotenv())


DB_USER = getenv("DB_USER")
DB_PASS = getenv("DB_PASS")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")







url: str = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
from sqlalchemy import insert
engine = create_engine(url=url, echo=True)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)