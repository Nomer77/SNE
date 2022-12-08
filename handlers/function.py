from aiogram import types

import markup
from config import bot, data, dashboard_buttons
import datetime
from aiogram.dispatcher import Dispatcher, FSMContext
from handlers.machine import FSMDashboard

async def set_message_id(state: FSMContext, m2u):
    async with state.proxy() as base:
        base['message_id'] = m2u.message_id

async def set_content_id(state: FSMContext, m2u):
    async with state.proxy() as base:
        base['content_id'] = m2u.message_id


async def delete_message(state: FSMContext, user):
    async with state.proxy() as base:
        await bot.delete_message(user, base['message_id'])

async def delete_content(state: FSMContext, user):
    async with state.proxy() as base:
        await bot.delete_message(user, base['content_id'])

def werkbank(message):
    message = message.strip()
    words = message.split(' ')
    try:
        datetime.datetime.strptime(words[len(words) - 1], '%H:%M')
        time = words[len(words) - 1]
        task = " ".join(words[:len(words) - 1])
    except ValueError:
        task = message
        time = None
    return task, time


async def umwandeln(state: FSMContext, value: str):
    try:
        async with state.proxy() as base:
            unbekannt = base[value]
    except KeyError:
        async with state.proxy() as base:
            base[value] = []
            unbekannt = base[value]
    return unbekannt


async def return_dashboard(state:FSMContext, user):
    await state.finish()
    await FSMDashboard.menu.set()
    m2u = await bot.send_message(user, "<i>Возвращаю вас в меню задач</i> \nВыберите нужный вам пункт", parse_mode='html', reply_markup=markup.buttons_list_return(dashboard_buttons))
    await set_message_id(state, m2u)




async def user_aufgabe_liste(user):
    all_task = await data.get_tasks(tele_id=user)
    if len(all_task) < 1:
        return "У вас нет задач..."
    complete_task = await data.get_tasks(tele_id=user, is_complete=1)
    noncomplete_task_without = await data.get_tasks(tele_id=user, is_complete=0, time=None)
    noncomplete_task = await data.get_tasks(tele_id=user, is_complete=0)
    ntw = []
    for value in noncomplete_task:
        if not value in noncomplete_task_without:
            ntw.append(value)
    for i in range(len(ntw)-1):
        for j in range(len(ntw)-i-1):
            if ntw[j][2] < ntw[j+1][2]:
                ntw[j], ntw[j+1] = ntw[j+1], ntw[j]
    message = "Ваш список задач: \n"
    count = 1
    for value in ntw:
        message += f"{count}. {value[1]} | {value[2]} \n"
        count += 1
    for value in noncomplete_task_without:
        message += f"{count}. {value[1]} \n"
        count += 1
    for value in complete_task:
        if value[2] is None:
            message += f"<s>{count}. {value[1]}</s> \n"
            count += 1
        else:
            message += f"<s>{count}. {value[1]} | {value[2]}</s> \n"
            count += 1
    return message








