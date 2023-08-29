from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from handlers.machine import *
from handlers.function import set_message_id, delete_message
from config import bot, menu_buttons
import markup

async def unrecognized_message(message: types.Message, state: FSMContext):
    if message.chat.id == message.from_user.id:
        m2u = await bot.send_message(message.from_user.id, "Возможно, ты потерялся... Хочешь верну тебя в меню?", reply_markup=markup.buttons_hope())
        if await state.get_state() is None:
            await FSMHope.hope.set()
            async with state.proxy() as base:
                base['save_state'] = True
        async with state.proxy() as base:
            base['hope_message'] = m2u.message_id


async def yes_answer(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Cмотри, а вот и оно...")
    await delete_message(state, callback_query.from_user.id)
    async with state.proxy() as base:
        await bot.delete_message(callback_query.from_user.id, base['hope_message'])
    await state.finish()
    await FSMLieter.menu.set()
    m2u = await bot.send_message(callback_query.from_user.id, "Выберите нужный вам пункт меню: ", reply_markup=markup.buttons_list(menu_buttons))
    await set_message_id(state, m2u)


async def no_answer(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as base:
        await bot.delete_message(callback_query.from_user.id, base['hope_message'])
        if 'save_state' in base:
            await state.finish()





def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(unrecognized_message, state='*')
    dp.register_callback_query_handler(yes_answer, lambda callback_query: callback_query.data == ':)', state='*')
    dp.register_callback_query_handler(no_answer, lambda callback_query: callback_query.data == '-_-', state='*')