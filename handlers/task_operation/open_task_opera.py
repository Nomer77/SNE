from aiogram import types
from aiogram.dispatcher import Dispatcher
from config_bot import data, bot
import markup


async def open_tasks(message: types.Message):
    if bool(await data.get_tasks(tele_id=message.from_user.id)):
        await bot.send_message(message.from_user.id, "Вот ваши задачи", reply_markup=markup.task_button())
        amount = 0
        noncom_task = {}
        for value in await data.get_tasks(tele_id=message.from_user.id, is_complete=0):
            noncom_task[value[0]] = await data.get_task_time(message.from_user.id, value[0])
        for k, v in noncom_task.items():
            if list(v[0])[0] is None:
                noncom_task[k] = -1
            else:
                noncom_task[k] = list(v[0])[0]
        sorted_task = dict(sorted(noncom_task.items(), key=lambda x: x[1]))
        for value in sorted_task:
            amount += 1
            await bot.send_message(message.from_user.id, f"{amount}. {value}")
        for value in await data.get_tasks(tele_id=message.from_user.id, is_complete=1):
            amount += 1
            await bot.send_message(message.from_user.id, f"<s>{amount}. <i>{value[0]}</i></s>", parse_mode='html')
    else:
        await bot.send_message(message.from_user.id, "У вас нет задач :(", reply_markup=markup.task_button())


def register_handlers_open_task(dp: Dispatcher):
    dp.register_message_handler(open_tasks, lambda message: message.text == 'Задачи')
