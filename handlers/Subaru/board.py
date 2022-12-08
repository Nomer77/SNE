from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from handlers.machine import FSMLieter, FSMBoard
from handlers.function import set_message_id, delete_message
from config import bot, service_buttons
import markup


async def subaru_board(callback_query: types.CallbackQuery, state: FSMContext):
    await FSMBoard.menu.set()
    m2u = await bot.send_message(callback_query.from_user.id, "Выберите нужный вам сервис: ", reply_markup=markup.buttons_list_return(service_buttons))
    await delete_message(state, callback_query.from_user.id)
    await set_message_id(state, m2u)



def register_board_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(subaru_board, lambda callback_query: callback_query.data == '0', state=FSMLieter.menu)