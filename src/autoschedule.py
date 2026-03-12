from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from oac import *
from main import TZ
from main import BACKEND_URL
from api import api_remote_call

def make_job(context: ContextTypes.DEFAULT_TYPE, callback, pattern, job_data, job_name):
    context.job_queue.run_repeating(callback, 
                                    interval=timedelta(weeks=1),
                                    first=TZ.localize(datetime.strptime(pattern, "%d.%m.%Y %H:%M")+timedelta(seconds=5)),
                                    data=job_data,
                                    name=job_name)


async def on_button_start_scheduling(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await api_remote_call(f"{BACKEND_URL}/user/register?fn={update.effective_user.full_name}&tid={update.effective_user.id}")
    discipline_name = context.user_data["name"]; date = context.user_data["date"]
    start_time = context.user_data["start_time"]; end_time = context.user_data["end_time"]

    LOGGER.info(f"User {update.effective_user.id} requested to schedule queue with discipline '{discipline_name}' (event: ON_BUTTON_START_SCHEDULING)")
    await api_remote_call(f"{BACKEND_URL}/queue?start_time={start_time.isoformat()}&date={date.isoformat()}")
    discipline = await api_remote_call(f"{BACKEND_URL}/discipline?date={date.isoformat()}&start_time={start_time.isoformat()}")
    week_day = discipline.get("week_day")
    queue = await api_remote_call(f"{BACKEND_URL}/queue?start_time={(start_time-timedelta(minutes=10)).isoformat()}&week_day={week_day}")

    o_string = f"{date}.{datetime.now().strftime('%Y')} {queue.get('start_time')}"
    o_job_name = f"ON_OPENED-{o_string}"
    a_string = f"{date}.{datetime.now().strftime('%Y')} {start_time.strftime('%H:%M')}"
    a_job_name = f"ON_ACTIVE-{a_string}"
    c_string = f"{date}.{datetime.now().strftime('%Y')} {end_time.strftime('%H:%M')}"
    c_job_name = f"ON_CLOSED-{c_string}"
    job_data = {"start_time": queue.get('start_time'), "week_day": week_day, "discipline_name": discipline_name}
    make_job(context, on_opened_queue, o_string, job_data, o_job_name)
    make_job(context, on_active_queue, a_string, job_data, a_job_name)
    make_job(context, on_closed_queue, c_string, job_data, c_job_name)
    await api_remote_call(f"{BACKEND_URL}/oac_jobs?start_time={(start_time-timedelta(minutes=10)).isoformat()}&week_day={week_day}&o_job_name={o_job_name}&a_job_name={a_job_name}&c_job_name={c_job_name}")
    await update.message.reply_text(text=f"Очередь '{discipline_name}' запланирована")


async def on_button_stop_scheduling(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass


async def autoschedule_on_start(context: ContextTypes.DEFAULT_TYPE) -> None:
    disciplines = await api_remote_call(f"{BACKEND_URL}/discipline/all")
    for d in disciplines:
        discipline_name = d.get("name")
        date = d.get("date")
        start_time = d.get("start_time")
        end_time = d.get("end_time")
        week_day = d.get("week_day")
        await api_remote_call(f"{BACKEND_URL}/queue?start_time={start_time}&date={date}")
        queue = await api_remote_call(f"{BACKEND_URL}/queue?start_time={start_time}&week_day={week_day}")
        
        o_string = f"{date} {queue.get('start_time')}"
        o_job_name = f"ON_OPENED-{o_string}"
        a_string = f"{date} {start_time}"
        a_job_name = f"ON_ACTIVE-{a_string}"
        c_string = f"{date} {end_time}"
        c_job_name = f"ON_CLOSED-{c_string}"
        job_data = {"start_time": queue.get('start_time'), "week_day": week_day, "discipline_name": discipline_name}
        make_job(context, on_opened_queue, o_string, job_data, o_job_name)
        make_job(context, on_active_queue, a_string, job_data, a_job_name)
        make_job(context, on_closed_queue, c_string, job_data, c_job_name)
        await api_remote_call(f"{BACKEND_URL}/oac_jobs?start_time={queue.get('start_time')}&week_day={week_day}&o_job_name={o_job_name}&a_job_name={a_job_name}&c_job_name={c_job_name}")
            


async def autoschedule_on_restart(context: ContextTypes.DEFAULT_TYPE) -> None:
    oac_jobs = await api_remote_call(f"{BACKEND_URL}/oac_jobs/all")
    for job in oac_jobs:
        queue = job.get("queue")
        discipline_name = queue.get("discipline").get("name")
        date = queue.get("discipline").get("date")
        start_time = queue.get("discipline").get("start_time")
        end_time = queue.get("discipline").get("end_time")
        week_day = queue.get("week_day")

        o_string = f"{date} {queue.get('start_time')}"
        o_job_name = job.get("a_job_name")
        a_string = f"{date} {start_time}"
        a_job_name = job.get("o_job_name")
        c_string = f"{date} {end_time}"
        c_job_name = job.get("c_job_name")
        job_data = {"start_time": queue.get('start_time'), "week_day": week_day, "discipline_name": discipline_name}
        make_job(context, on_opened_queue, o_string, job_data, o_job_name)
        make_job(context, on_active_queue, a_string, job_data, a_job_name)
        make_job(context, on_closed_queue, c_string, job_data, c_job_name)