from aiogram import types
from aiogram.dispatcher import Dispatcher
from config_bot import data
import markup
from loguru import logger


# @dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.answer(f"{message.chat.username}, Добро пожаловать!", reply_markup=markup.menu_buttons())
    if not await data.is_user_exists(message.from_user.id):
        await data.add_user(message.from_user.id)
        logger.info(f"Bot created new user ({message.from_user.id})")


# @dp.message_handler(commands=['menu'])
async def command_menu(message: types.Message):
    await message.answer("Уже открыл!", reply_markup=markup.menu_buttons())
    logger.info(f"User ({message.from_user.id}) {message.from_user.username} opened menu")


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_menu, commands=['menu'])
    dp.register_message_handler(command_menu, lambda message: message.text == "Меню")
