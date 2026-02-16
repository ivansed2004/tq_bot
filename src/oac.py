from telegram.ext import ContextTypes
from datetime import datetime
from applog import LOGGER


async def on_opened_queue(context: ContextTypes.DEFAULT_TYPE) -> None:
    start_time = context.job.data["start_time"]
    week_day = context.job.data["week_day"]
    discipline_name = context.job.data["discipline_name"]
    users_to_notify = get_queue_subscribers( datetime.strptime(start_time, "%H:%M"), week_day )
    update_queue_state( datetime.strptime(start_time, "%H:%M"), week_day )
    notification_text = f"Через 10 минут ожидается начало дисциплины '{discipline_name}'. Очередь открыта для заполнения"
    LOGGER.info(f"Queue for discipline {discipline_name} opened.' (event: ON_OPENED_QUEUE)")
    for user in users_to_notify:
        await context.bot.send_message(chat_id=user.chat_id, text=notification_text)


async def on_active_queue(context: ContextTypes.DEFAULT_TYPE) -> None:
    start_time = context.job.data["start_time"]
    week_day = context.job.data["week_day"]
    discipline_name = context.job.data["discipline_name"]
    update_queue_state( datetime.strptime(start_time, "%H:%M"), week_day )
    LOGGER.info(f"Queue for discipline {discipline_name} activated.' (event: ON_ACTIVE_QUEUE)")


async def on_closed_queue(context: ContextTypes.DEFAULT_TYPE) -> None:
    start_time = context.job.data["start_time"]
    week_day = context.job.data["week_day"]
    discipline_name = context.job.data["discipline_name"]
    update_queue_state( datetime.strptime(start_time, "%H:%M"), week_day )
    empty_queue( datetime.strptime(start_time, "%H:%M"), week_day )
    LOGGER.info(f"Queue for discipline {discipline_name} closed.' (event: ON_CLOSED_QUEUE)")