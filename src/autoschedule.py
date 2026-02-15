from telegram import Update
from telegram.ext import ContextTypes
from data_access import (
    get_all_oac_jobs, get_all_disciplines,
    get_discipline_by_date_time,
    save_new_queue_with_discipline, 
    save_new_oac_jobs_with_queue,
    get_queue_by_time_week_day, 
    save_new_queue_with_discipline
)
from models import Discipline, OACJobs
from datetime import datetime, timedelta
from oac import *
from main import TZ
from utils import authenticate


def make_job(context: ContextTypes.DEFAULT_TYPE, callback, pattern, job_data, job_name):
    context.job_queue.run_repeating(callback, 
                                    interval=timedelta(weeks=1),
                                    first=TZ.localize(datetime.strptime(pattern, "%d.%m.%Y %H:%M")+timedelta(seconds=5)),
                                    data=job_data,
                                    name=job_name)


async def on_button_start_scheduling(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    authenticate(update.effective_user.full_name, update.effective_user.id)
    discipline_name = context.user_data["name"]; date = context.user_data["date"]
    start_time = context.user_data["start_time"]; end_time = context.user_data["end_time"]

    LOGGER.info(f"User {update.effective_user.id} requested to schedule queue with discipline '{discipline_name}' (event: ON_BUTTON_START_SCHEDULING)")
    save_new_queue_with_discipline( start_time, date )
    discipline = get_discipline_by_date_time( date, start_time )
    week_day = discipline.week_day
    queue = get_queue_by_time_week_day( start_time-timedelta(minutes=10), week_day )

    o_string = f"{date}.{datetime.now().strftime('%Y')} {queue.start_time.strftime('%H:%M')}"
    o_job_name = f"ON_OPENED-{o_string}"
    a_string = f"{date}.{datetime.now().strftime('%Y')} {start_time.strftime('%H:%M')}"
    a_job_name = f"ON_ACTIVE-{a_string}"
    c_string = f"{date}.{datetime.now().strftime('%Y')} {end_time.strftime('%H:%M')}"
    c_job_name = f"ON_CLOSED-{c_string}"
    job_data = {"start_time": queue.start_time.strftime('%H:%M'), "week_day": week_day, "discipline_name": discipline_name}
    make_job(context, on_opened_queue, o_string, job_data, o_job_name)
    make_job(context, on_active_queue, a_string, job_data, a_job_name)
    make_job(context, on_closed_queue, c_string, job_data, c_job_name)
    save_new_oac_jobs_with_queue(start_time-timedelta(minutes=10), week_day, o_job_name, a_job_name, c_job_name)
    await update.message.reply_text(text=f"Очередь '{discipline_name}' запланирована")


async def on_button_stop_scheduling(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass


async def autoschedule_on_start(context: ContextTypes.DEFAULT_TYPE) -> None:
    disciplines: list[Discipline] = get_all_disciplines()
    for d in disciplines:
        discipline_name = d.name; date = d.date
        start_time = d.start_time; end_time = d.end_time
        week_day = d.week_day
        save_new_queue_with_discipline(start_time, date)
        queue = get_queue_by_time_week_day(start_time-timedelta(minutes=10), week_day)
        
        o_string = f"{date.strftime('%d.%m')}.{datetime.now().strftime('%Y')} {queue.start_time.strftime('%H:%M')}"
        o_job_name = f"ON_OPENED-{o_string}"
        a_string = f"{date.strftime('%d.%m')}.{datetime.now().strftime('%Y')} {start_time.strftime('%H:%M')}"
        a_job_name = f"ON_ACTIVE-{a_string}"
        c_string = f"{date.strftime('%d.%m')}.{datetime.now().strftime('%Y')} {end_time.strftime('%H:%M')}"
        c_job_name = f"ON_CLOSED-{c_string}"
        job_data = {"start_time": queue.start_time.strftime('%H:%M'), "week_day": week_day, "discipline_name": discipline_name}
        make_job(context, on_opened_queue, o_string, job_data, o_job_name)
        make_job(context, on_active_queue, a_string, job_data, a_job_name)
        make_job(context, on_closed_queue, c_string, job_data, c_job_name)
        save_new_oac_jobs_with_queue(queue.start_time, week_day, o_job_name, a_job_name, c_job_name)
            


async def autoschedule_on_restart(context: ContextTypes.DEFAULT_TYPE) -> None:
    oac_jobs: list[OACJobs] = get_all_oac_jobs()
    for job in oac_jobs:
        queue = job.queue
        discipline_name = queue.discipline.name; date = queue.discipline.date
        start_time = queue.discipline.start_time; end_time = queue.discipline.end_time
        week_day = queue.week_day

        o_string = f"{date.strftime('%d.%m')}.{datetime.now().strftime('%Y')} {queue.start_time.strftime('%H:%M')}"
        o_job_name = job.a_job_name
        a_string = f"{date.strftime('%d.%m')}.{datetime.now().strftime('%Y')} {start_time.strftime('%H:%M')}"
        a_job_name = job.o_job_name
        c_string = f"{date.strftime('%d.%m')}.{datetime.now().strftime('%Y')} {end_time.strftime('%H:%M')}"
        c_job_name = job.c_job_name
        job_data = {"start_time": queue.start_time.strftime('%H:%M'), "week_day": week_day, "discipline_name": discipline_name}
        make_job(context, on_opened_queue, o_string, job_data, o_job_name)
        make_job(context, on_active_queue, a_string, job_data, a_job_name)
        make_job(context, on_closed_queue, c_string, job_data, c_job_name)