import enum
from typing import Deque, List
from sqlalchemy import (
    String, Enum, Integer, BigInteger, 
    DateTime, Table, Column, ForeignKey, 
    PrimaryKeyConstraint
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped,
    mapped_column, relationship
)
from sqlalchemy.types import PickleType


class QueueState(enum.Enum):
    OPENED = "Открытая"
    CLOSED = "Закрытая"


class Base(DeclarativeBase):
    pass


queue_user_at = Table('queue_user_at', Base.metadata,
    Column('q_id', BigInteger, ForeignKey("queue.id"), nullable=False),
    Column('user_id', BigInteger, ForeignKey("user.id"), nullable=False),
    PrimaryKeyConstraint("q_id", "user_id")
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    fullname: Mapped[str] = mapped_column(String)
    queues: Mapped[List["Queue"]] = relationship("Queue", back_populates="subscribers", lazy="joined", cascade="save-update", secondary=queue_user_at)

    def __eq__(self, other):
        if isinstance(other, User):
            return self.telegram_id == other.telegram_id
        return False

    def __hash__(self):
        return hash(self.telegram_id)


class Discipline(Base):
    __tablename__ = "discipline"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    number: Mapped[str] = mapped_column(String)
    start_time: Mapped[DateTime] = mapped_column(DateTime)
    end_time: Mapped[DateTime] = mapped_column(DateTime)
    date: Mapped[DateTime] = mapped_column(DateTime)
    week_day: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    teacher: Mapped[str] = mapped_column(String, nullable=True)
    location: Mapped[str] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(String)

    def __eq__(self, other):
        if isinstance(other, Discipline):
            return (self.start_time, self.date) == (other.start_time, other.date)
        return False

    def __hash__(self):
        return hash(self.start_time, self.date)

    def __str__(self):
        return (
            f"Порядковый номер: {self.number}\n"
            f"Время начала: {self.start_time.strftime('%H:%M')}\n"
            f"Время окончания: {self.end_time.strftime('%H:%M')}\n"
            f"Наименование: {self.name}\n"
            f"Дата: {self.week_day}, {self.date.strftime('%d.%m')}\n"
            f"Преподаватель: {self.teacher}\n"
            f"Аудитория: {self.location}\n"
            f"Тип: {self.type}"
        )


class Queue(Base):
    __tablename__ = "queue"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    start_time: Mapped[DateTime] = mapped_column(DateTime)
    week_day: Mapped[str] = mapped_column(String)
    dscp_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("discipline.id"))
    discipline: Mapped["Discipline"] = relationship()
    state: Mapped[QueueState] = mapped_column(Enum(QueueState))
    size: Mapped[int] = mapped_column(Integer)
    content: Mapped[Deque] = mapped_column(PickleType)
    subscribers: Mapped[List["User"]] = relationship("User", back_populates="queues", lazy="joined", cascade="save-update", secondary=queue_user_at)

    def __eq__(self, other):
        if isinstance(other, Queue):
            return (self.start_time, self.week_day) == (other.start_time, other.week_day)
        return False

    def __hash__(self):
        return hash(self.start_time, self.week_day)

    def __str__(self) -> str:
        queue_positioned = [ f"{i+1}. {user.fullname}" for i, user in enumerate(self.content) ]
        return "\n".join((
            f"Оповещение о начале каждые: {self.week_day}, {self.start_time.strftime('%H:%M')}",
            f"Статус: {self.state.value}",
            f"Размер: {self.size}",
            f"\n\n ~== ОБЪЕКТ ПЛАНИРОВАНИЯ ==~ \n\n"
            f"{self.discipline}",
            "Список пользователей:",
            "\n".join(queue_positioned)
        ))
    

class OACJobs(Base):
    __tablename__ = "oac_jobs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    o_job_name: Mapped[object] = mapped_column(String, nullable=False)
    a_job_name: Mapped[object] = mapped_column(String, nullable=False)
    c_job_name: Mapped[object] = mapped_column(String, nullable=False)
    q_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("queue.id"))
    queue: Mapped["Queue"] = relationship(backref="oac_jobs")

    def __eq__(self, other):
        if isinstance(other, OACJobs):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)