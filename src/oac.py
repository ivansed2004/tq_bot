from telegram.ext import ContextTypes
from applog import LOGGER
from api import api_remote_call
from main import BACKEND_URL


async def on_opened_queue(context: ContextTypes.DEFAULT_TYPE) -> None:
    start_time = context.job.data["start_time"]
    week_day = context.job.data["week_day"]
    discipline_name = context.job.data["discipline_name"]
    users_to_notify = await api_remote_call(f"{BACKEND_URL}/queue/subscribers?start_time={start_time}&week_day={week_day}")
    await api_remote_call(f"{BACKEND_URL}/queue/state?start_time={start_time}&week_day={week_day}")
    notification_text = f"Через 10 минут ожидается начало дисциплины '{discipline_name}'. Очередь открыта для заполнения"
    LOGGER.info(f"Queue for discipline {discipline_name} opened.' (event: ON_OPENED_QUEUE)")
    for user in users_to_notify:
        await context.bot.send_message(chat_id=user.get("chat_id"), text=notification_text)


async def on_active_queue(context: ContextTypes.DEFAULT_TYPE) -> None:
    start_time = context.job.data["start_time"]
    week_day = context.job.data["week_day"]
    discipline_name = context.job.data["discipline_name"]
    await api_remote_call(f"{BACKEND_URL}/queue/state?start_time={start_time}&week_day={week_day}")
    LOGGER.info(f"Queue for discipline {discipline_name} activated.' (event: ON_ACTIVE_QUEUE)")


async def on_closed_queue(context: ContextTypes.DEFAULT_TYPE) -> None:
    start_time = context.job.data["start_time"]
    week_day = context.job.data["week_day"]
    discipline_name = context.job.data["discipline_name"]
    await api_remote_call(f"{BACKEND_URL}/queue/state?start_time={start_time}&week_day={week_day}")
    await api_remote_call(f"{BACKEND_URL}/queue/empty?start_time={start_time}&week_day={week_day}")
    LOGGER.info(f"Queue for discipline {discipline_name} closed.' (event: ON_CLOSED_QUEUE)")