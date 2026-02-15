from typing import List
from collections import deque
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.orm.attributes import flag_modified
from models import *
from os import getenv
from applog import LOGGER 
from datetime import timedelta


DATABASE_URL = getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
LOGGER.info("Connection established and tables created.")


def save_new_discipline(disc: Discipline):
    with Session(engine) as session:
        LOGGER.info(f"ORM 'save_new_discipline' method has been invoked")
        discipline = session.query(Discipline).filter_by(start_time=disc.start_time, date=disc.date).first()
        if not discipline:
            session.add(disc)
        session.commit()


def save_all_disciplines(discs: list[Discipline]) -> None:
    with Session(engine) as session:
        LOGGER.info(f"ORM 'save_all_disciplines' method has been invoked")
        session.add_all(discs)
        session.commit()


def get_queue_by_time_week_day(start_time, week_day) -> Queue:
    with Session(engine) as session:
        LOGGER.info(f"ORM 'get_queue_by_time_week_day' method has been invoked")
        return session.query(Queue).options(selectinload(Queue.discipline)).filter_by(start_time=start_time, week_day=week_day).first()


def save_user_registered(fullname_: str, tid: int) -> None:
    with Session(engine) as session:
        LOGGER.info(f"ORM 'save_user_registered' method has been invoked")
        user = session.query(User).filter_by(telegram_id=tid).first()
        if not user:
            session.add( User(fullname=fullname_, telegram_id=tid) )
        session.commit()


def save_new_queue_with_discipline(start_time, date) -> None:
    with Session(engine) as session:
        LOGGER.info(f"ORM 'save_new_queue_with_discipline' method has been invoked")
        disc = session.query(Discipline).filter_by(date=date, start_time=start_time).first()
        s_time = disc.start_time - timedelta(minutes=10)
        queue = Queue(start_time=s_time,
                      week_day=disc.week_day,
                      discipline=disc,
                      state=QueueState.CLOSED,
                      size=0,
                      content=deque())
        session.add(queue)
        session.commit()
    

def save_new_oac_jobs_with_queue(start_time, week_day, o_job_name, a_job_name, c_job_name) -> None:
    with Session(engine) as session:
        LOGGER.info(f"ORM 'save_new_oac_jobs_with_queue' method has been invoked")
        queue = session.query(Queue).filter_by(start_time=start_time, week_day=week_day).first()
        oac_jobs = OACJobs(o_job_name=o_job_name, a_job_name=a_job_name, c_job_name=c_job_name, queue=queue)
        session.add(oac_jobs)
        session.commit()


def put_subscriber_into_queue(start_time, week_day, tid):
    LOGGER.info(f"ORM 'put_subscriber_into_queue' method has been invoked")
    with Session(engine) as session:
        user = session.query(User).filter_by(telegram_id=tid).first()
        queue = session.query(Queue).options(selectinload(Queue.subscribers)).filter_by(start_time=start_time, week_day=week_day).first()
        q_subscribers = queue.subscribers
        if (user not in q_subscribers):
            q_subscribers.append(user)
        session.commit()


def get_user_by_telegram_id(tid: int) -> User:
    with Session(engine) as session:
        LOGGER.info(f"ORM 'get_user_by_telegram_id' method has been invoked")
        return session.query(User).filter_by(telegram_id=tid).first()


def get_all_users() -> List[User]:
    with Session(engine) as session:
        LOGGER.info(f"ORM 'get_all_users' method has been invoked")
        return session.query(User).all()


def get_queues(regime: str) -> List[Queue]:
    with Session(engine) as session:
        LOGGER.info(f"ORM 'get_all_queues' method has been invoked")
        current_session = session.query(Queue).options(selectinload(Queue.discipline))
        if (regime == "ALL"):
            return current_session.all()
        else:
            return current_session.filter_by(state=QueueState.OPENED).all()
        

def get_queue_state(start_time, week_day) -> QueueState:
    with Session(engine) as session:
        LOGGER.info(f"ORM 'get_queue_state' method has been invoked")
        queue = session.query(Queue).filter_by(start_time=start_time, week_day=week_day).first()
        return queue.state


def get_all_disciplines() -> List[Discipline]:
    with Session(engine) as session:
        LOGGER.info(f"ORM 'get_all_disciplines' method has been invoked")
        disciplines = session.query(Discipline).all()
        return disciplines


def get_all_oac_jobs() -> List[OACJobs]:
    with Session(engine) as session:
        LOGGER.info(f"ORM 'get_all_oac_jobs' method has been invoked")
        return session.query(OACJobs).options(selectinload(OACJobs.queue).selectinload(Queue.discipline)).all()
    

def get_queue_by_time_week_day(start_time, week_day) -> Queue:
    with Session(engine) as session:
        LOGGER.info(f"ORM 'get_queue_by_time_week_day' method has been invoked")
        return session.query(Queue).options(selectinload(Queue.discipline)).filter_by(start_time=start_time, week_day=week_day).first()


def get_discipline_by_date_time(date, start_time) -> Discipline:
    with Session(engine) as session:
        LOGGER.info(f"ORM 'get_discipline_by_date_time' method has been invoked")
        return session.query(Discipline).filter_by(date=date, start_time=start_time).first()
    

def get_queue_subscribers( start_time, week_day ) -> list[User]:
    with Session(engine) as session:
        queue = session.query(Queue).options(selectinload(Queue.subscribers)).filter_by(start_time=start_time, week_day=week_day).first()
        LOGGER.info(f"ORM 'get_queue_subscribers' method has been invoked")
        return queue.subscribers


def get_subscribed_queues_by_user(tid) -> list[Queue]:
    with Session(engine) as session:
        user = session.query(User).options(selectinload(User.queues).selectinload(Queue.discipline)).filter_by(telegram_id=tid).first()
        LOGGER.info(f"ORM 'get_subscribed_queues_by_user' method has been invoked")
        return user.queues


def remove_subsriber_from_queue(start_time, week_day, tid):
    LOGGER.info(f"ORM 'remove_subsriber_from_queue' method has been invoked")
    with Session(engine) as session:
        user = session.query(User).filter_by(telegram_id=tid).first()
        queue = session.query(Queue).options(selectinload(Queue.subscribers)).filter_by(start_time=start_time, week_day=week_day).first()
        q_subscribers = queue.subscribers
        if (user in q_subscribers):
            q_subscribers.remove(user)
        session.commit()


def empty_queue( start_time, week_day ):
    with Session(engine) as session:
        queue = session.query(Queue).filter_by(start_time=start_time, week_day=week_day).first()
        if (queue.state == QueueState.CLOSED):
            queue.content = deque()
            queue.size = 0
        session.commit()
        

def update_queue_with_discipline(start_time, week_day, d: Discipline) -> None:
    with Session(engine) as session:
        LOGGER.info(f"ORM 'update_queue_discipline' method has been invoked")
        queue = session.query(Queue).options(selectinload(Queue.discipline)).filter_by(start_time=start_time, week_day=week_day).first()
        if queue:
            d1 = queue.discipline
            queue.discipline = d
            session.delete(d1)
        else:
            queue = Queue(start_time=start_time,
                      week_day=week_day,
                      discipline=d,
                      state=QueueState.CLOSED,
                      size=0,
                      content=deque())
            session.add(queue)
        session.commit()


def update_queue_state( start_time, week_day ) -> None:
    with Session(engine) as session:
        queue = session.query(Queue).filter_by(start_time=start_time, week_day=week_day).first()
        LOGGER.info(f"ORM 'update_queue_state' method has been invoked")
        if queue:
            if (queue.state == QueueState.CLOSED):
                queue.state = QueueState.OPENED
            else:
                queue.state = QueueState.CLOSED
        session.commit()


def append_to_queue(start_time, week_day, tid) -> tuple:
    with Session(engine) as session:
        LOGGER.info(f"ORM 'append_to_queue' method has been invoked")
        queue = session.query(Queue).filter_by(start_time=start_time, week_day=week_day).first()
        if ( not (queue.state == QueueState.CLOSED) ):
            user = session.query(User).filter_by(telegram_id=tid).first()
            position = 0
            if user not in queue.content:
                queue.content.append(user)
                flag_modified(queue, "content")
                position = queue.size + 1
                queue.size = position
                session.commit()
                return ("yes", position)
            else:
                position = queue.content.index(user)+1
                return ("no", position)
        else:
            return ("closed", -1)


def remove_from_queue(start_time, week_day, tid) -> tuple:
    with Session(engine) as session:
        LOGGER.info(f"ORM 'remove_from_queue' method has been invoked")
        queue = session.query(Queue).filter_by(start_time=start_time, week_day=week_day).first()
        if ( not (queue.state == QueueState.CLOSED) ):
            user = session.query(User).filter_by(telegram_id=tid).first()
            if user in queue.content:
                position = queue.content.index(user)+1
                queue.content.remove(user)
                queue.size = queue.size - 1
                flag_modified(queue, "content")
                session.commit()
                return ("yes", position)
            return ("no", 0)
        else:
            return ("closed", -1)