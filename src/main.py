import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler,
    MessageHandler, filters,
    ContextTypes
)
from utils import *
from datetime import datetime
from os import getenv
from applog import LOGGER
from oac import *
import pytz
from autoschedule import *
from api import api_remote_call

# Bot token
BOT_TOKEN = getenv('TELEGRAM_QUEUING_BOT')
BACKEND_URL = getenv('BACKEND_URL')
TZ = pytz.timezone('Europe/Moscow')


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await api_remote_call(f"{BACKEND_URL}/user/register?fn={update.effective_user.full_name}&tid={update.effective_user.id}")
    LOGGER.info(f"User {update.effective_user.id} invoked /start or menu (event: MENU)")
    markup = ReplyKeyboardMarkup( get_menu_keyboard(), resize_keyboard=True )
    await update.message.reply_text("Управление очередями:", reply_markup=markup)
    LOGGER.info(f"User {update.effective_user.id} menu has been sent")


async def on_menu_button_list_queues(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await api_remote_call(f"{BACKEND_URL}/user/register?fn={update.effective_user.full_name}&tid={update.effective_user.id}")
    LOGGER.info(f"User {update.effective_user.id} requested available queues to be listed (event: ON_MENU_BUTTON_LIST_QUEUES)")
    keyboard = get_listed_queues_keyboard("ALL", "Открыть")
    LOGGER.info(f"User {update.effective_user.id} available queues has been taken (orm: get_queues)")
    if (keyboard == []):
        await update.message.reply_text("Нет очередей")
        LOGGER.info(f"User {update.effective_user.id} has taken no available queues")
    else:
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Доступные очереди:", reply_markup=markup)
        LOGGER.info(f"User {update.effective_user.id} available queues has been sent")


async def on_menu_button_list_opened_queues(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await api_remote_call(f"{BACKEND_URL}/user/register?fn={update.effective_user.full_name}&tid={update.effective_user.id}")
    LOGGER.info(f"User {update.effective_user.id} requested opened queues to be listed (event: ON_MENU_BUTTON_LIST_OPENED_QUEUES)")
    keyboard = get_listed_queues_keyboard("O", "Открыть")
    LOGGER.info(f"User {update.effective_user.id} opened queues has been taken (orm: get_queues)")
    if (keyboard == []):
        await update.message.reply_text("Нет открытых очередей")
        LOGGER.info(f"User {update.effective_user.id} has taken no opened queues")
    else:
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Открытые очереди:", reply_markup=markup)
        LOGGER.info(f"User {update.effective_user.id} opened queues has been sent")


async def on_button_queue_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await api_remote_call(f"{BACKEND_URL}/user/register?fn={update.effective_user.full_name}&tid={update.effective_user.id}")
    text = update.message.text.split("   ")
    queue_name = text[1][1:-1]; week_day = text[2]
    start_time = text[3]; start_time = datetime.strptime(start_time, "%H:%M")
    LOGGER.info(f"User {update.effective_user.id} requested to open queue '{queue_name}' (event: ON_BUTTON_QUEUE_INFO)")
    queue = await api_remote_call(f"{BACKEND_URL}/queue?week_day={week_day}&start_time={start_time.strftime('%H:%M')}")
    LOGGER.info(f"User {update.effective_user.id} queue '{queue_name}' has been taken (orm: get_queue_by_time_week_day)")
    markup = ReplyKeyboardMarkup( get_queue_info_keyboard(start_time, week_day, "К очередям"), resize_keyboard=True )
    await update.message.reply_text(f"{queue}", reply_markup=markup)
    context.user_data["queue_name"] = queue_name 
    context.user_data["time"] = start_time; context.user_data["week_day"] = week_day
    LOGGER.info(f"User {update.effective_user.id} has taken queue '{queue_name}' info")


async def on_menu_button_scheduling_queue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await api_remote_call(f"{BACKEND_URL}/user/register?fn={update.effective_user.full_name}&tid={update.effective_user.id}")
    LOGGER.info(f"User {update.effective_user.id} requested available disciplines to be listed (event: ON_MENU_BUTTON_SCHEDULING_QUEUES)")
    keyboard = get_listed_disciplines_keyboard()
    LOGGER.info(f"User {update.effective_user.id} available disciplines has been taken (orm: get_all_disciplines)")
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Доступные дисциплины:", reply_markup=markup)
    LOGGER.info(f"User {update.effective_user.id} available disciplines has been sent")


async def on_button_discipline_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await api_remote_call(f"{BACKEND_URL}/user/register?fn={update.effective_user.full_name}&tid={update.effective_user.id}")
    text = update.message.text.split("   ")
    discipline_name = text[0][1:-1]
    time = text[1].split("-")
    start_time = time[0]; start_time = datetime.strptime(start_time, "%H:%M")
    end_time = time[1]; end_time = datetime.strptime(end_time, "%H:%M")
    date = text[2]; date = datetime.strptime(date, "%d.%m")
    LOGGER.info(f"User {update.effective_user.id} requested to open discipline '{discipline_name}' (event: ON_BUTTON_DISCIPLINE_INFO)")
    discipline = await api_remote_call(f"{BACKEND_URL}/discipline?date={date.strftime('%d.%m')}&start_time={start_time.strftime('%H:%M')}")
    LOGGER.info(f"User {update.effective_user.id} discipline '{discipline_name}' has been taken (orm: get_discipline_by_date_time)")
    markup = ReplyKeyboardMarkup( get_discipline_info_keyboard(), resize_keyboard=True )
    await update.message.reply_text(f"{ discipline_info(discipline) }", reply_markup=markup)
    context.user_data["name"] = discipline_name; context.user_data["date"] = date
    context.user_data["start_time"] = start_time; context.user_data["end_time"] = end_time
    LOGGER.info(f"User {update.effective_user.id} has taken discipline '{discipline_name}' info")


async def on_menu_button_my_queues(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await api_remote_call(f"{BACKEND_URL}/user/register?fn={update.effective_user.full_name}&tid={update.effective_user.id}")
    LOGGER.info(f"User {update.effective_user.id} requested to queues he subscribed to (event: ON_MENU_BUTTON_MY_QUEUES)")
    keyboard = get_users_subscribed_queues_keyboard(update.effective_user.id)
    LOGGER.info(f"User {update.effective_user.id} queues have been taken (orm: get_subscribed_queues_by_user)")
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Очереди с подписками:", reply_markup=markup)
    LOGGER.info(f"User {update.effective_user.id} queues have been sent")


async def on_menu_button_enter_queue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await api_remote_call(f"{BACKEND_URL}/user/register?fn={update.effective_user.full_name}&tid={update.effective_user.id}")
    LOGGER.info(f"User {update.effective_user.id} requested to enter a queue (event: ON_MENU_BUTTON_ENTER_QUEUE)")
    keyboard = get_listed_queues_keyboard("O", "Встать")
    LOGGER.info(f"User {update.effective_user.id} available queues have been taken (orm: get_queues)")
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите очередь:", reply_markup=markup)
    LOGGER.info(f"User {update.effective_user.id} available queues have been sent")


async def on_button_enter_queue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await api_remote_call(f"{BACKEND_URL}/user/register?fn={update.effective_user.full_name}&tid={update.effective_user.id}")
    queue_name = context.user_data["queue_name"]
    start_time = context.user_data["time"]
    week_day = context.user_data["week_day"]
    LOGGER.info(f"User {update.effective_user.id} has chosen queue '{queue_name}' to enter (event: ON_BUTTON_ENTER_QUEUE)")
    response_json = await api_remote_call(f"{BACKEND_URL}/queue/append?week_day={week_day}&start_time={start_time.strftime('%H:%M')}&tid={update.effective_user.id}")
    answer = response_json["answer"]; position = response_json["position"]
    LOGGER.info(f"User {update.effective_user.id} has been added to queue '{queue_name}' on position '{position}' (orm: append_to_queue)")
    if (answer == "yes"):
        await update.message.reply_text(f"Вы встали в очередь '{queue_name}' на позицию '{position}'")
        LOGGER.info(f"User {update.effective_user.id} has taken successful entering message")
    elif (answer == "no"):
        await update.message.reply_text(f"Вы уже состоите в очереди '{queue_name}' на позиции '{position}'")
        LOGGER.info(f"User {update.effective_user.id} has taken 'already in queue' message")
    else:
        await update.message.reply_text(f"Очередь '{queue_name}' закрыта")
        LOGGER.info(f"User {update.effective_user.id} has tried to enter to closed queue")


async def on_menu_button_leave_queue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await api_remote_call(f"{BACKEND_URL}/user/register?fn={update.effective_user.full_name}&tid={update.effective_user.id}")
    LOGGER.info(f"User {update.effective_user.id} requested to exit a queue (event: ON_MENU_BUTTON_LEAVE_QUEUE)")
    keyboard = get_listed_queues_keyboard("O", "Покинуть")
    LOGGER.info(f"User {update.effective_user.id} available queues has been taken (orm: get_queues)")
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите очередь:", reply_markup=markup)
    LOGGER.info(f"User {update.effective_user.id} available queues has been sent")


async def on_button_leave_queue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await api_remote_call(f"{BACKEND_URL}/user/register?fn={update.effective_user.full_name}&tid={update.effective_user.id}")
    queue_name = context.user_data["queue_name"]
    start_time = context.user_data["time"]
    week_day = context.user_data["week_day"]
    LOGGER.info(f"User {update.effective_user.id} has chosen queue '{queue_name}' to exit (event: ON_BUTTON_LEAVE_QUEUE)")
    response_json = await api_remote_call(f"{BACKEND_URL}/queue/pop?week_day={week_day}&start_time={start_time.strftime('%H:%M')}&tid={update.effective_user.id}")
    answer = response_json["answer"]; position = response_json["position"]
    LOGGER.info(f"User {update.effective_user.id} has released position '{position}' of queue '{queue_name}' (orm: pop_from_queue)")
    if (answer == "yes"):
        await update.message.reply_text(f"Вы освободили позицию '{position}' в очереди '{queue_name}'")
        LOGGER.info(f"User {update.effective_user.id} has taken successful exiting message")
    elif (answer == "no"):
        await update.message.reply_text(f"Вы не состоите в очереди '{queue_name}'")
        LOGGER.info(f"User {update.effective_user.id} has taken 'not in queue' message")
    else:
        await update.message.reply_text(f"Очередь '{queue_name}' закрыта")
        LOGGER.info(f"User {update.effective_user.id} has tried to enter to closed queue")


async def on_button_update_queue_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await api_remote_call(f"{BACKEND_URL}/user/register?fn={update.effective_user.full_name}&tid={update.effective_user.id}")
    queue_name = context.user_data["queue_name"]
    start_time =  context.user_data["time"]; week_day = context.user_data["week_day"]
    LOGGER.info(f"User {update.effective_user.id} requested to update queue '{queue_name}' (event: ON_BUTTON_UPDATE_QUEUE_INFO)")
    queue = await api_remote_call(f"{BACKEND_URL}/queue?week_day={week_day}&start_time={start_time.strftime('%H:%M')}")
    LOGGER.info(f"User {update.effective_user.id} queue '{queue_name}' has been taken (orm: get_queue_by_time_week_day)")
    markup = ReplyKeyboardMarkup( get_queue_info_keyboard(start_time, week_day, "К моим очередям"), resize_keyboard=True )
    await update.message.reply_text(f"{ queue_info(queue) }", reply_markup=markup)
    LOGGER.info(f"User {update.effective_user.id} has taken queue '{queue_name}' info updated")


async def on_button_subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await api_remote_call(f"{BACKEND_URL}/user/register?fn={update.effective_user.full_name}&tid={update.effective_user.id}")
    queue_name = context.user_data["queue_name"]
    start_time = context.user_data["time"]; week_day = context.user_data["week_day"]
    LOGGER.info(f"User {update.effective_user.id} requested to subscribe to queue '{queue_name}' (event: ON_BUTTON_SUBSCRIBE)")
    queue = await api_remote_call(f"{BACKEND_URL}/queue?week_day={week_day}&start_time={start_time.strftime('%H:%M')}")
    LOGGER.info(f"User {update.effective_user.id} queue '{queue_name}' has been taken (orm: get_queue_by_time_week_day)")
    user = await api_remote_call(f"{BACKEND_URL}/user?tid={update.effective_user.id}")
    LOGGER.info(f"User {update.effective_user.id}'s object has been taken (orm: get_user_by_telegram_id)")
    if (user not in queue.subscribers):
        await api_remote_call(f"{BACKEND_URL}/queue/subscriber/put?week_day={week_day}&start_time={start_time.strftime('%H:%M')}&tid={update.effective_user.id}")
        LOGGER.info(f"User {update.effective_user.id} subscribed to queue '{queue_name}' (orm: put_subscriber_into_queue)")
        await update.message.reply_text(text=f"Вы подписались на уведомления об очереди '{queue_name}'")
        markup = ReplyKeyboardMarkup( get_queue_info_keyboard(start_time, week_day, "К очередям"), resize_keyboard=True )
        await update.message.reply_text(f"{ queue_info(queue) }", reply_markup=markup)
    else:
        LOGGER.info(f"User {update.effective_user.id} already subscribed to queue '{queue_name}'")
        await update.message.reply_text(text=f"Вы уже подписаны")


async def on_button_unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await api_remote_call(f"{BACKEND_URL}/user/register?fn={update.effective_user.full_name}&tid={update.effective_user.id}")
    queue_name = context.user_data["queue_name"]
    start_time = context.user_data["time"]; week_day = context.user_data["week_day"]
    LOGGER.info(f"User {update.effective_user.id} requested to unsubscribe to queue '{queue_name}' (event: ON_BUTTON_UNSUBSCRIBE)")
    queue = await api_remote_call(f"{BACKEND_URL}/queue?week_day={week_day}&start_time={start_time.strftime('%H:%M')}")
    LOGGER.info(f"User {update.effective_user.id} queue '{queue_name}' has been taken (api: get_queue_by_time_week_day)")
    user = await api_remote_call(f"{BACKEND_URL}/user?tid={update.effective_user.id}")
    LOGGER.info(f"User {update.effective_user.id}'s object has been taken (api: get_user_by_telegram_id)")
    if (user in queue.subscribers):
        api_remote_call(f"{BACKEND_URL}/queue/subscriber/remove?week_day={week_day}&start_time={start_time.strftime('%H:%M')}&tid={update.effective_user.id}")
        LOGGER.info(f"User {update.effective_user.id} unsubscribed from queue '{queue_name}' (api: remove_subsriber_from_queue)")
        await update.message.reply_text(text=f"Вы отказались от уведомлений об очереди '{queue_name}'")
    else:
        LOGGER.info(f"User {update.effective_user.id} is not in queue '{queue_name} yet' (orm: remove_subsriber_from_queue)")
        await update.message.reply_text(text=f"Вы не подписаны")


async def start_queuing_bot() -> None:
    LOGGER.info("Bot has been initialization started")
    application = Application.builder().token(BOT_TOKEN).build()
    LOGGER.info("Bot has been initialization completed")
    application.add_handler(CommandHandler("start", menu))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🏛В меню$"), menu))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🔙К очередям$"), on_menu_button_list_queues))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🔙К моим очередям$"), on_menu_button_my_queues))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🔙К открытым очередям$"), on_menu_button_list_opened_queues))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🔙К дисциплинам$"), on_menu_button_scheduling_queue))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Открыть"), on_button_queue_info))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^⬆️Встать в очередь$"), on_menu_button_enter_queue))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^⬆️Встать$"), on_button_enter_queue))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Встать"), on_button_enter_queue))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^⬇️Покинуть очередь$"), on_menu_button_leave_queue))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^⬇️Покинуть$"), on_button_leave_queue))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^Покинуть"), on_button_leave_queue))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🔄Обновить$"), on_button_update_queue_info))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🔔Подписаться$"), on_button_subscribe))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🔕Отписаться$"), on_button_unsubscribe))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^📄Все очереди$"), on_menu_button_list_queues))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🗓Планирование очередей$"), on_menu_button_scheduling_queue))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^'"), on_button_discipline_info))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^✅Начать планирование$"), on_button_start_scheduling))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^❌Остановить планирование$"), on_button_stop_scheduling))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🏠Мои очереди$"), on_menu_button_my_queues))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🆗Открытые очереди$"), on_menu_button_list_opened_queues))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    oac_jobs = api_remote_call(f"{BACKEND_URL}/oac_jobs/all")
    if ( len(oac_jobs) == 0 ):
        application.job_queue.run_once(autoschedule_on_start, when=0)
    else:
        application.job_queue.run_once(autoschedule_on_restart, when=0)
    try:
        await asyncio.Future()
    except KeyboardInterrupt:
        await application.updater.stop()
        await application.stop()
        LOGGER.info("Bot has been stopped")


if __name__ == "__main__":
    asyncio.run( start_queuing_bot() )
