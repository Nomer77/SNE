from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from handlers.machine import FSMLieter, FSMDashboard
from handlers.function import delete_message, set_message_id
from config import data, bot, dashboard_buttons
import markup


async def dashboard_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await FSMDashboard.menu.set()
    m2u = await bot.send_message(callback_query.from_user.id, "Выберите нужный вам пункт \n"
                                                              "<i>Здесь вы можете взаимодействовать c задачами </i>",
                                parse_mode='html', reply_markup=markup.buttons_list_return(dashboard_buttons))
    await delete_message(state, callback_query.from_user.id)
    await set_message_id(state, m2u)


def register_dashboard_handler(dp: Dispatcher):
    dp.register_callback_query_handler(dashboard_menu, lambda callback_query: callback_query.data == '1', state=FSMLieter.menu)