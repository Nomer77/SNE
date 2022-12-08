from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from handlers.function import umwandeln, set_message_id, delete_message, return_dashboard, werkbank
from handlers.machine import FSMDashboard, FSMEdit
from config import data, bot
import markup


async def auswalh_task(callback_query: types.CallbackQuery, state: FSMContext):
    await FSMEdit.auswalh.set()
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
    m2u = await bot.send_message(callback_query.from_user.id, "Выберите задачу, которую хотите изменить: ", reply_markup=markup.buttons_special_data(for_buttons))
    await delete_message(state, callback_query.from_user.id)
    await set_message_id(state, m2u)
    await FSMEdit.annahme.set()


async def annahme_task(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as base:
        unperformed = base['unperformed']
    for value in unperformed:
        if callback_query.data == str(value[0]):
            async with state.proxy() as base:
                edit_id = callback_query.data
                base['edit_id'] = edit_id
    m2u = await bot.send_message(callback_query.from_user.id, f"Введите одним сообщением задачу на которую вы хотите поменять выбранную задачу.",
                                 reply_markup=markup.button_cancel())
    await delete_message(state, callback_query.from_user.id)
    await set_message_id(state, m2u)
    await FSMEdit.falte.set()


async def senden_edit(message: types.Message, state: FSMContext):
    await FSMEdit.submit.set()
    async with state.proxy() as base:
        edit_id = base['edit_id']
    new_task, new_time = werkbank(message.text)
    await data.update_task(edit_id, new_task, new_time)
    if new_time is None:
        m2u = await bot.send_message(message.from_user.id, f"Задача обновлена на <u>{new_task}</u>", parse_mode='html', reply_markup=markup.button_return())
    else:
        m2u = await bot.send_message(message.from_user.id, f"Задача обновлена на <u>{new_task}</u> с временем <u>{new_time}</u>", parse_mode='html', reply_markup=markup.button_return())
    await delete_message(state, message.from_user.id)
    await set_message_id(state, m2u)



def register_edit_handler(dp: Dispatcher):
    dp.register_callback_query_handler(auswalh_task, lambda callback_query: callback_query.data == '3', state=FSMDashboard.menu)
    dp.register_callback_query_handler(annahme_task, state=FSMEdit.annahme)
    dp.register_message_handler(senden_edit, state=FSMEdit.falte)