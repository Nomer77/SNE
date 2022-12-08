from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
import markup
from handlers.function import umwandeln, set_message_id, delete_message, return_dashboard
from handlers.machine import FSMDashboard, FSMComplete
from config import data, bot


async def auswalh_task(callback_query: types.CallbackQuery, state: FSMContext):
    await FSMComplete.auswalh.set()
    unperformed = await data.get_tasks(tele_id=callback_query.from_user.id, is_complete=0)
    if len(unperformed) < 1:
        m2u = await bot.send_message(callback_query.from_user.id, "У вас нет незаконченных задач", reply_markup=markup.button_return())
        await delete_message(state, callback_query.from_user.id)
        await set_message_id(state, m2u)
        return 0
    async with state.proxy() as base:
        base['unperformed'] = unperformed
    for_buttons = []
    for value in unperformed:
        for_buttons.append([(lambda task, time: task if time is None else f"{task} | {time}" )(value[1], value[2]), value[0]])
    m2u = await bot.send_message(callback_query.from_user.id, "Выберите задачу, которую хотите отметить выполненной: ", reply_markup=markup.buttons_special_data(for_buttons))
    await delete_message(state, callback_query.from_user.id)
    await set_message_id(state, m2u)
    await FSMComplete.submit.set()


async def senden_complete(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as base:
        unperformed = base['unperformed']
    for value in unperformed:
        if callback_query.data == str(value[0]):
            await data.set_complete(callback_query.from_user.id, value[0])
            if value[2] is None:
                m2u = await bot.send_message(callback_query.from_user.id, f"Задача <u>{value[1]}</u> успешно отмечена выполненной", parse_mode='html', reply_markup=markup.button_return())
            else:
                m2u = await bot.send_message(callback_query.from_user.id, f"Задача <u>{value[1]}</u> на время <u>{value[2]}</u> успешно отмечена выполненной", parse_mode='html', reply_markup=markup.button_return())
            await delete_message(state, callback_query.from_user.id)
            await set_message_id(state, m2u)



def register_complete_handler(dp: Dispatcher):
    dp.register_callback_query_handler(auswalh_task, lambda callback_query: callback_query.data == '2', state=FSMDashboard.menu)
    dp.register_callback_query_handler(senden_complete, state=FSMComplete.submit)