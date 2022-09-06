from aiogram import types
from aiogram.dispatcher import Dispatcher
from config_bot import bot
import markup


# @dp.message_handler(lambda message: message.text == "Редактировать")
async def edit_task_menu(message: types.Message):
    await bot.send_message(message.from_user.id, "Ыгы", reply_markup=markup.edit_task_button())


def register_handlers_edit_task_menu(dp: Dispatcher):
    dp.register_message_handler(edit_task_menu, lambda message: message.text == "Редактировать")