from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from handlers.function import umwandeln, set_message_id, delete_message, return_dashboard
from handlers.machine import FSMDashboard, FSMDelete
from config import data, bot
import markup


async def auswalh_task(callback_query: types.CallbackQuery, state: FSMContext):
    await FSMDelete.auswalh.set()
    all_task = await data.get_tasks(tele_id=callback_query.from_user.id)
    if len(all_task) < 1:
        m2u = await bot.send_message(callback_query.from_user.id, "У вас нету задач", reply_markup=markup.button_return())
        await delete_message(state, callback_query.from_user.id)
        await set_message_id(state, m2u)
        return 0
    async with state.proxy() as base:
        base['all_task'] = all_task
    for_buttons = []
    for value in all_task:
        for_buttons.append([(lambda task, time: task if time is None else f"{task} | {time}" )(value[1], value[2]), value[0]])
    m2u = await bot.send_message(callback_query.from_user.id, "Выберите задачу, которую хотите удалить: ", reply_markup=markup.buttons_special_data(for_buttons))
    await delete_message(state, callback_query.from_user.id)
    await set_message_id(state, m2u)
    await FSMDelete.submit.set()

async def senden_delete(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as base:
        all_task = base['all_task']
    for value in all_task:
        if callback_query.data == str(value[0]):
            await data.delete_task(callback_query.from_user.id, value[0])
            if value[2] is None:
                m2u = await bot.send_message(callback_query.from_user.id, f"Задача <u>{value[1]}</u> успешно удалена", parse_mode='html', reply_markup=markup.button_return())
            else:
                m2u = await bot.send_message(callback_query.from_user.id, f"Задача <u>{value[1]}</u> на время <u>{value[2]}</u> успешно удалена", parse_mode='html', reply_markup=markup.button_return())
            await delete_message(state, callback_query.from_user.id)
            await set_message_id(state, m2u)


def register_delete_handler(dp: Dispatcher):
    dp.register_callback_query_handler(auswalh_task, lambda callback_query: callback_query.data == '4', state=FSMDashboard.menu)
    dp.register_callback_query_handler(senden_delete, state=FSMDelete.submit)