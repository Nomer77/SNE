from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from handlers.machine import FSMLieter
from handlers.function import set_message_id, user_aufgabe_liste
from config import bot, data, menu_buttons
import markup
import pycbrf
import asyncio


async def command_start(message: types.Message):
    if message.from_user.id == message.chat.id:
        welcome = open('gif_message/welcome.mp4', 'rb')
        if message.from_user.last_name is None:
            await types.ChatActions.upload_video_note()
            await asyncio.sleep(1)
            await bot.send_video_note(message.from_user.id, welcome)
            await message.answer("Добро пожаловать!", reply_markup=markup.checkout())
        else:
            await types.ChatActions.upload_video_note()
            await asyncio.sleep(1)
            await bot.send_video_note(message.from_user.id, welcome)
            await message.answer(f"{message.from_user.first_name}, Добро пожаловать!", reply_markup=markup.checkout())
        if not await data.is_user_exists(message.from_user.id):
            await message.answer("Я буду менеджером твоих задач. В мои задачи входит напоминать тебе о них, быть твоей записной книжкой и многое другое. \n"
                                 "Полную информацию обо мне можешь узнать прописав комманду /help")
            await data.add_user(message.from_user.id)
    else:
        await message.answer("Приветсвую! Для моей полноценной работы, перейди в личный чат со мной")

async def command_menu(message: types.Message, state: FSMContext):
    if message.from_user.id == message.chat.id:
        await FSMLieter.menu.set()
        m2u = await bot.send_message(message.from_user.id, "Выберите нужный вам пункт меню: ", reply_markup=markup.buttons_list(menu_buttons))
        await set_message_id(state, m2u)
    else:
        await message.answer("Для моей полноценной работы, перейди в личный чат со мной")

async def command_help(message: types.Message):
    if message.from_user.id == message.chat.id:
        await message.answer("Это бот создан быть менеджером ваших задач. Вы можете выйти в главное меню командой /menu \n"
                             "Перейдя в раздел задачи из главного меню, вы сможете взаимодействовать со списком задач: добавлять, удалять, выполнять и редактировать задачи")
    else:
        await message.answer("Для моей полноценной работы, перейди в личный чат со мной")


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_menu, commands=['menu'])
    dp.register_message_handler(command_menu, lambda message: message.text == "Вызвать меню")
    dp.register_message_handler(command_help, commands=['help'])

