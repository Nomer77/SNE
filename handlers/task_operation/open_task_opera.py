from aiogram import types
from aiogram.dispatcher import Dispatcher
from config_bot import data, bot
import markup


async def open_tasks(message: types.Message):
    if bool(await data.get_tasks(tele_id=message.from_user.id)):
        await bot.send_message(message.from_user.id, "Вот ваши задачи", reply_markup=markup.task_button())
        amount = 0
        for value in await data.get_tasks(tele_id=message.from_user.id, is_complete=0):
            amount += 1
            await bot.send_message(message.from_user.id, f"{amount}. {value[0]}")
        for value in await data.get_tasks(tele_id=message.from_user.id, is_complete=1):
            amount += 1
            await bot.send_message(message.from_user.id, f"<s>{amount}. <i>{value[0]}</i></s>", parse_mode='html')
    else:
        await bot.send_message(message.from_user.id, "У вас нету задач :(", reply_markup=markup.task_button())


def register_handlers_open_task(dp: Dispatcher):
    dp.register_message_handler(open_tasks, lambda message: message.text == 'Задачи')
