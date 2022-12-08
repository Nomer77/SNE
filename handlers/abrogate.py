from aiogram import types
from config import bot, menu_buttons, dashboard_buttons
import markup
from aiogram.dispatcher import Dispatcher, FSMContext
from handlers.function import delete_message, set_message_id, delete_content
from handlers.machine import *


async def cancel_action(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, "Действие отменено.", reply_markup=markup.checkout())
    await delete_message(state, callback_query.from_user.id)
    await state.finish()

async def return_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await FSMLieter.menu.set()
    try:
        await delete_content(state, callback_query.from_user.id)
    except Exception:
        pass
    m2u = await bot.send_message(callback_query.from_user.id, "<i>Возвращаю вас в меню...</i> \nВыберите нужный вам пункт меню: ", parse_mode='html', reply_markup=markup.buttons_list(menu_buttons))
    await delete_message(state, callback_query.from_user.id)
    await set_message_id(state, m2u)

async def return_dashboard(callback_query: types.CallbackQuery, state: FSMContext):
    await delete_message(state, callback_query.from_user.id)
    try:
        await delete_content(state, callback_query.from_user.id)
    except Exception:
        pass
    await state.finish()
    await FSMDashboard.menu.set()
    m2u = await bot.send_message(callback_query.from_user.id, "<i>Возвращаю вас в меню задач</i> \nВыберите нужный вам пункт", parse_mode='html', reply_markup=markup.buttons_list_return(dashboard_buttons))
    await set_message_id(state, m2u)


def register_abrogate_handler(dp: Dispatcher):
    #Menu

    dp.register_callback_query_handler(cancel_action, lambda callback_query: callback_query.data == '-1', state=FSMLieter.menu)

    #Dashboard

    dp.register_callback_query_handler(return_menu, lambda callback_query: callback_query.data == '-1', state=FSMDashboard.menu)

    #Nachtrag

    dp.register_callback_query_handler(return_dashboard, lambda callback_query: callback_query.data == '-1', state=FSMNachtrag.description)
    dp.register_callback_query_handler(return_dashboard, lambda callback_query: callback_query.data == '-1', state=FSMNachtrag.annahme)
    dp.register_callback_query_handler(return_dashboard, lambda callback_query: callback_query.data == '-1', state=FSMNachtrag.submit)

    #Complete

    dp.register_callback_query_handler(return_dashboard, lambda callback_query: callback_query.data == '-1', state=FSMComplete.auswalh)
    dp.register_callback_query_handler(return_dashboard, lambda callback_query: callback_query.data == '-1', state=FSMComplete.submit)

    #Delete

    dp.register_callback_query_handler(return_dashboard, lambda callback_query: callback_query.data == '-1', state=FSMDelete.auswalh)
    dp.register_callback_query_handler(return_dashboard, lambda callback_query: callback_query.data == '-1', state=FSMDelete.submit)

    #Edit

    dp.register_callback_query_handler(return_dashboard, lambda callback_query: callback_query.data == '-1', state=FSMEdit.auswalh)
    dp.register_callback_query_handler(return_dashboard, lambda callback_query: callback_query.data == '-1', state=FSMEdit.annahme)
    dp.register_callback_query_handler(return_dashboard, lambda callback_query: callback_query.data == '-1', state=FSMEdit.falte)
    dp.register_callback_query_handler(return_dashboard, lambda callback_query: callback_query.data == '-1', state=FSMEdit.submit)

    #Liste

    dp.register_callback_query_handler(return_dashboard, lambda callback_query: callback_query.data == '-1', state=FSMListe.submit)

    #Feedback

    dp.register_callback_query_handler(return_dashboard, lambda callback_query: callback_query.data == '-1', state=FSMFeedback.annahme)
    dp.register_callback_query_handler(return_dashboard, lambda callback_query: callback_query.data == '-1', state=FSMFeedback.submit)

    #Board

    dp.register_callback_query_handler(return_menu, lambda callback_query: callback_query.data == '-1', state=FSMBoard.menu)

    dp.register_callback_query_handler(return_menu, lambda callback_query: callback_query.data == '-1', state=FSMValute.auswalh)
    dp.register_callback_query_handler(return_menu, lambda callback_query: callback_query.data == '-1', state=FSMValute.submit)

