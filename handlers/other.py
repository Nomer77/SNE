from aiogram import types
from aiogram.dispatcher import Dispatcher
from config_bot import bot
import markup


# @dp.message_handler()
async def unrecognized_message(message: types.Message):
    await bot.send_message(message.from_user.id, "Сообщение не распознано или на команде стоит заглушка",
                           reply_markup=markup.menu_buttons())


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(unrecognized_message)
