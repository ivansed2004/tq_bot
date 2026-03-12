from telegram import KeyboardButton
from main import BACKEND_URL
from api import api_remote_call


def get_menu_keyboard():
    return [
        [ KeyboardButton("🏠Мои очереди") ],
        [ KeyboardButton("🆗Открытые очереди") ],
        [ KeyboardButton("📄Все очереди") ],
        [ KeyboardButton("🗓Планирование очередей") ],
        [
            KeyboardButton("⬆️Встать в очередь"),
            KeyboardButton("⬇️Покинуть очередь")
        ]
    ]


async def get_queue_info_keyboard(start_time, week_day, action_name):
    state = await api_remote_call(f"{BACKEND_URL}/queue/state?start_time={start_time}&week_day={week_day}")
    if ( state.value == "Открытая" ):
        return [
            [ KeyboardButton("⬆️Встать") ],
            [ KeyboardButton("⬇️Покинуть") ],
            [ KeyboardButton("🔄Обновить") ],
            [   
                KeyboardButton("🔔Подписаться"),
                KeyboardButton("🔕Отписаться")
            ],
            [
                KeyboardButton(f"🔙{action_name}"),
                KeyboardButton("🏛В меню")
            ]
        ]
    else:
        return [
            [   
                KeyboardButton("🔔Подписаться"),
                KeyboardButton("🔕Отписаться")
            ],
            [
                KeyboardButton(f"🔙{action_name}"),
                KeyboardButton("🏛В меню")
            ]
        ]


async def get_listed_queues_keyboard(regime: str, action_name: str):
    queues = await api_remote_call(f"{BACKEND_URL}/queues?regime={regime}")
    keyboard = [ [KeyboardButton(f"{action_name}   '{q.discipline.name}'   {q.week_day}   {q.start_time.strftime('%H:%M')}")] for q in queues ]
    keyboard.append( [KeyboardButton("🏛В меню")] )
    return keyboard


async def get_users_subscribed_queues_keyboard(tid):
    queues = await api_remote_call(f"{BACKEND_URL}/user/queues?tid={tid}")
    keyboard = [ [KeyboardButton(f"Открыть   '{q.discipline.name}'   {q.week_day}   {q.start_time.strftime('%H:%M')}")] for q in queues ]
    keyboard.append( [KeyboardButton("🏛В меню")] )
    return keyboard


async def get_listed_disciplines_keyboard():
    disciplines = await api_remote_call(f"{BACKEND_URL}/discipline/all")
    keyboard = [ [KeyboardButton(f"'{d.name}'   {d.start_time.strftime('%H:%M')}-{d.end_time.strftime('%H:%M')}   {d.date.strftime('%d.%m')}")] for d in disciplines ]  
    keyboard.append( [KeyboardButton("🏛В меню")] )
    return keyboard


def get_discipline_info_keyboard():
    return [
        [ KeyboardButton("✅Начать планирование") ],
        [ KeyboardButton("❌Остановить планирование") ],
        [
            KeyboardButton("🔙К дисциплинам"),
            KeyboardButton("🏛В меню")
        ]
    ]


def discipline_info(discipline):
    return (
        f"Порядковый номер: {discipline.number}\n"
        f"Время начала: {discipline.start_time.strftime('%H:%M')}\n"
        f"Время окончания: {discipline.end_time.strftime('%H:%M')}\n"
        f"Наименование: {discipline.name}\n"
        f"Дата: {discipline.week_day}, {discipline.date.strftime('%d.%m')}\n"
        f"Преподаватель: {discipline.teacher}\n"
        f"Аудитория: {discipline.location}\n"
        f"Тип: {discipline.type}"
    )


def queue_info(queue):
    queue_positioned = [ f"{i+1}. {user.fullname}" for i, user in enumerate(queue.content) ]
    return "\n".join((
        f"Оповещение о начале каждые: {queue.week_day}, {queue.start_time.strftime('%H:%M')}",
        f"Статус: {queue.state.value}",
        f"Размер: {queue.size}",
        f"\n\n ~== ОБЪЕКТ ПЛАНИРОВАНИЯ ==~ \n\n"
        f"{queue.discipline}",
        "Список пользователей:",
        "\n".join(queue_positioned)
    ))