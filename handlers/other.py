from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from handlers.machine import *
from handlers.function import set_message_id, delete_message
from config import bot, menu_buttons
import markup

async def unrecognized_message(message: types.Message, state: FSMContext):
    if message.chat.id == message.from_user.id:
        m2u = await bot.send_message(message.from_user.id, "Возможно, ты потерялся... Хочешь верну тебя в меню?", reply_markup=markup.buttons_hope())
        try:
            async with state.proxy() as base:
                base['hope_message'] = m2u.message_id
        except Exception:
            await FSMHope.hope.set()
            async with state.proxy() as base:
                base['hope_message'] = m2u.message_id
                base['state_bool'] = True

async def yes_answer(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Cмотри, а вот и оно...")
    try:
        await delete_message(state, callback_query.from_user.id)
    except Exception:
        pass
    async with state.proxy() as base:
        await bot.delete_message(callback_query.from_user.id, base['hope_message'])
    await state.finish()
    await FSMLieter.menu.set()
    m2u = await bot.send_message(callback_query.from_user.id, "Выберите нужный вам пункт меню: ", reply_markup=markup.buttons_list(menu_buttons))
    await set_message_id(state, m2u)


async def no_answer(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as base:
        await bot.delete_message(callback_query.from_user.id, base['hope_message'])
        try:
            bool = base['state_bool']
            await state.finish()
        except Exception:
            pass





def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(unrecognized_message)
    dp.register_message_handler(unrecognized_message, state=FSMLieter.menu)
    dp.register_message_handler(unrecognized_message, state=FSMDashboard.menu)
    dp.register_message_handler(unrecognized_message, state=FSMNachtrag.submit)
    dp.register_message_handler(unrecognized_message, state=FSMComplete.auswalh)
    dp.register_message_handler(unrecognized_message, state=FSMComplete.submit)
    dp.register_message_handler(unrecognized_message, state=FSMEdit.auswalh)
    dp.register_message_handler(unrecognized_message, state=FSMEdit.submit)
    dp.register_message_handler(unrecognized_message, state=FSMDelete.auswalh)
    dp.register_message_handler(unrecognized_message, state=FSMDelete.submit)
    dp.register_message_handler(unrecognized_message, state=FSMListe.submit)
    dp.register_message_handler(unrecognized_message, state=FSMFeedback.submit)
    dp.register_message_handler(unrecognized_message, state=FSMBoard.menu)
    dp.register_message_handler(unrecognized_message, state=FSMValute.auswalh)
    dp.register_message_handler(unrecognized_message, state=FSMValute.submit)

    dp.register_callback_query_handler(yes_answer, lambda callback_query: callback_query.data == ':)')
    dp.register_callback_query_handler(yes_answer, lambda callback_query: callback_query.data == ':)', state=FSMLieter.menu)
    dp.register_callback_query_handler(yes_answer, lambda callback_query: callback_query.data == ':)', state=FSMDashboard.menu)
    dp.register_callback_query_handler(yes_answer, lambda callback_query: callback_query.data == ':)', state=FSMNachtrag.submit)
    dp.register_callback_query_handler(yes_answer, lambda callback_query: callback_query.data == ':)', state=FSMComplete.auswalh)
    dp.register_callback_query_handler(yes_answer, lambda callback_query: callback_query.data == ':)', state=FSMComplete.submit)
    dp.register_callback_query_handler(yes_answer, lambda callback_query: callback_query.data == ':)', state=FSMEdit.auswalh)
    dp.register_callback_query_handler(yes_answer, lambda callback_query: callback_query.data == ':)', state=FSMEdit.submit)
    dp.register_callback_query_handler(yes_answer, lambda callback_query: callback_query.data == ':)', state=FSMDelete.auswalh)
    dp.register_callback_query_handler(yes_answer, lambda callback_query: callback_query.data == ':)', state=FSMDelete.submit)
    dp.register_callback_query_handler(yes_answer, lambda callback_query: callback_query.data == ':)', state=FSMListe.submit)
    dp.register_callback_query_handler(yes_answer, lambda callback_query: callback_query.data == ':)', state=FSMFeedback.submit)
    dp.register_callback_query_handler(yes_answer, lambda callback_query: callback_query.data == ':)', state=FSMBoard.menu)
    dp.register_callback_query_handler(yes_answer, lambda callback_query: callback_query.data == ':)', state=FSMValute.auswalh)
    dp.register_callback_query_handler(yes_answer, lambda callback_query: callback_query.data == ':)', state=FSMValute.submit)


    dp.register_callback_query_handler(no_answer, lambda callback_query: callback_query.data == '-_-',)
    dp.register_callback_query_handler(no_answer, lambda callback_query: callback_query.data == '-_-', state=FSMLieter.menu)
    dp.register_callback_query_handler(no_answer, lambda callback_query: callback_query.data == '-_-', state=FSMDashboard.menu)
    dp.register_callback_query_handler(no_answer, lambda callback_query: callback_query.data == '-_-', state=FSMNachtrag.submit)
    dp.register_callback_query_handler(no_answer, lambda callback_query: callback_query.data == '-_-', state=FSMComplete.auswalh)
    dp.register_callback_query_handler(no_answer, lambda callback_query: callback_query.data == '-_-', state=FSMComplete.submit)
    dp.register_callback_query_handler(no_answer, lambda callback_query: callback_query.data == '-_-', state=FSMEdit.auswalh)
    dp.register_callback_query_handler(no_answer, lambda callback_query: callback_query.data == '-_-', state=FSMEdit.submit)
    dp.register_callback_query_handler(no_answer, lambda callback_query: callback_query.data == '-_-', state=FSMDelete.auswalh)
    dp.register_callback_query_handler(no_answer, lambda callback_query: callback_query.data == '-_-', state=FSMDelete.submit)
    dp.register_callback_query_handler(no_answer, lambda callback_query: callback_query.data == '-_-', state=FSMListe.submit)
    dp.register_callback_query_handler(no_answer, lambda callback_query: callback_query.data == '-_-', state=FSMFeedback.submit)
    dp.register_callback_query_handler(no_answer, lambda callback_query: callback_query.data == '-_-', state=FSMBoard.menu)
    dp.register_callback_query_handler(no_answer, lambda callback_query: callback_query.data == '-_-', state=FSMValute.auswalh)
    dp.register_callback_query_handler(no_answer, lambda callback_query: callback_query.data == '-_-', state=FSMValute.submit)
