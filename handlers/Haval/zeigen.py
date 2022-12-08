from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from handlers.function import delete_message, user_aufgabe_liste, return_dashboard, set_message_id
from handlers.machine import FSMDashboard, FSMListe
import markup
from config import bot

async def senden_list(callback_query: types.CallbackQuery, state: FSMContext):
    await FSMListe.submit.set()
    message = await user_aufgabe_liste(callback_query.from_user.id)
    m2u = await bot.send_message(callback_query.from_user.id, message, parse_mode='html', reply_markup=markup.button_return())
    await delete_message(state, callback_query.from_user.id)
    await set_message_id(state, m2u)

def register_zeigen_handler(dp: Dispatcher):
    dp.register_callback_query_handler(senden_list, lambda callback_query: callback_query.data == '0', state=FSMDashboard.menu)