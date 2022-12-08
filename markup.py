from aiogram import types

def checkout():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    call_button = types.KeyboardButton("Вызвать меню")
    markup.add(call_button)
    return markup


def buttons_list(data: list):
    markup = types.InlineKeyboardMarkup(row_width=1)
    count = 0
    for value in data:
        button = types.InlineKeyboardButton(value, callback_data=str(count))
        markup.add(button)
        count += 1
    cancel_button = types.InlineKeyboardButton("Отменить 🚫", callback_data='-1')
    markup.add(cancel_button)
    return markup


def buttons_list_return(data: list):
    markup = types.InlineKeyboardMarkup(row_width=1)
    count = 0
    for value in data:
        button = types.InlineKeyboardButton(value, callback_data=str(count))
        markup.add(button)
        count += 1
    cancel_button = types.InlineKeyboardButton("Вернуться в меню ↩️", callback_data='-1')
    markup.add(cancel_button)
    return markup

def button_cancel():
    markup = types.InlineKeyboardMarkup(row_width=1)
    cancel_button = types.InlineKeyboardButton("Отменить 🚫", callback_data='-1')
    markup.add(cancel_button)
    return markup


def buttons_special_data(data: list):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for value in data:
        button = types.InlineKeyboardButton(value[0], callback_data=str(value[1]))
        markup.add(button)
    cancel_button = types.InlineKeyboardButton("Отменить 🚫", callback_data='-1')
    markup.add(cancel_button)
    return markup


def button_return():
    markup = types.InlineKeyboardMarkup(row_width=1)
    return_button = types.InlineKeyboardButton("Вернуться в меню ↩️", callback_data='-1')
    markup.add(return_button)
    return markup

def buttons_hope():
    markup = types.InlineKeyboardMarkup(row_width=1)
    yes_button = types.InlineKeyboardButton("Вернуться 🏠", callback_data=':)')
    no_button = types.InlineKeyboardButton("Неа", callback_data='-_-')
    markup.add(yes_button, no_button)
    return markup

# def menu_buttons():
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     custom = types.KeyboardButton("Персонализация")
#     tasks = types.KeyboardButton("Задачи")
#     feedback = types.KeyboardButton("Обратная связь")
#     markup.add(custom, tasks, feedback)
#     return markup
#
#
# def task_button():
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     complete = types.KeyboardButton("Выполнить")
#     add = types.KeyboardButton("Добавить задачи")
#     edit = types.KeyboardButton("Редактировать")
#     menu = types.KeyboardButton("Меню")
#     markup.add(complete, add, edit, menu)
#     return markup
#
#
# def edit_task_button():
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     delete = types.KeyboardButton("Удалить задачу")
#     edit = types.KeyboardButton("Редактировать задачу")
#     menu = types.KeyboardButton("Меню")
#     markup.row(delete, edit).add(menu)
#     return markup
#
#
# def stop_adding_button():
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     stop = types.KeyboardButton("Стоп")
#     markup.add(stop)
#     return markup
#
#
# def cancel_button():
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     stop = types.KeyboardButton("Отменить")
#     markup.add(stop)
#     return markup
#
#
# async def choose_task(tasks, tele_id):
#     markup = types.InlineKeyboardMarkup(row_width=1)
#     for value in tasks:
#         button_task = types.InlineKeyboardButton(value[0], callback_data=await data.get_task_id(tele_id, value[0]))
#         markup.add(button_task)
#     button_cancel = types.InlineKeyboardButton("Отменить", callback_data='0')
#     markup.add(button_cancel)
#     return markup
