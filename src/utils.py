from telegram import KeyboardButton


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


def get_queue_info_keyboard(start_time, week_day, action_name):
    state = get_queue_state(start_time, week_day)
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


def get_listed_queues_keyboard(regime: str, action_name: str):
    keyboard = [ [KeyboardButton(f"{action_name}   '{q.discipline.name}'   {q.week_day}   {q.start_time.strftime('%H:%M')}")] for q in get_queues(regime) ]
    keyboard.append( [KeyboardButton("🏛В меню")] )
    return keyboard


def get_users_subscribed_queues_keyboard(tid):
    keyboard = [ [KeyboardButton(f"Открыть   '{q.discipline.name}'   {q.week_day}   {q.start_time.strftime('%H:%M')}")] for q in get_subscribed_queues_by_user(tid) ]
    keyboard.append( [KeyboardButton("🏛В меню")] )
    return keyboard


def get_listed_disciplines_keyboard():
    keyboard = [ [KeyboardButton(f"'{d.name}'   {d.start_time.strftime('%H:%M')}-{d.end_time.strftime('%H:%M')}   {d.date.strftime('%d.%m')}")] for d in get_all_disciplines() ]  
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