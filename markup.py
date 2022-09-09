from aiogram import types


def menu_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    custom = types.KeyboardButton("Персонализация")
    tasks = types.KeyboardButton("Задачи")
    feedback = types.KeyboardButton("Обратная связь")
    markup.add(custom, tasks, feedback)
    return markup


def task_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    complete = types.KeyboardButton("Выполнить")
    add = types.KeyboardButton("Добавить задачи")
    edit = types.KeyboardButton("Редактировать")
    menu = types.KeyboardButton("Меню")
    markup.add(complete, add, edit, menu)
    return markup


def edit_task_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    delete = types.KeyboardButton("Удалить задачу")
    edit = types.KeyboardButton("Редактировать задачу")
    menu = types.KeyboardButton("Меню")
    markup.row(delete, edit).add(menu)
    return markup


def stop_adding_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stop = types.KeyboardButton("Стоп")
    markup.add(stop)
    return markup


def cancel_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stop = types.KeyboardButton("Отменить")
    markup.add(stop)
    return markup


def choose_task(tasks):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for value in tasks:
        button_task = types.InlineKeyboardButton(value[0], callback_data=value[0])
        markup.add(button_task)
    button_cancel = types.InlineKeyboardButton("Отменить", callback_data='0')
    markup.add(button_cancel)
    return markup
