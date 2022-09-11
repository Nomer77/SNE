from aiogram import types
from aiogram.dispatcher import Dispatcher
from config_bot import data
import markup
from loguru import logger
from handlers.task_operation.open_task_opera import open_tasks


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
    if not await data.is_user_exists(message.from_user.id):
        await data.add_user(message.from_user.id)
        logger.info(f"Bot created new user ({message.from_user.id})")


async def command_task_list(message: types.Message):
    await open_tasks(message)
    logger.info(f"User ({message.from_user.id}) {message.from_user.username} took task list")


async def command_help(message: types.Message):
    await message.answer("Это бот создан быть менеджером ваших задач. Вы можете выйти в главное меню командой /menu")
    await message.answer("Вы можете получить список ваших задач командой /tasklist. Перейдя в раздел задачи из "
                         "главного меню, вы сможете взаимодействовать с этим списком: добавлять, удалять, выполнять и "
                         "редактировать задачи")
    if not await data.is_user_exists(message.from_user.id):
        await data.add_user(message.from_user.id)
        logger.info(f"Bot created new user ({message.from_user.id})")


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_menu, commands=['menu'])
    dp.register_message_handler(command_task_list, commands=['tasklist'])
    dp.register_message_handler(command_menu, lambda message: message.text == "Меню")
