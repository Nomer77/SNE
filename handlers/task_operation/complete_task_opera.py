from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher, FSMContext
from config_bot import bot, data
import markup


class FSM_complete_task(StatesGroup):
    choose_complete = State()


# @dp.message_handlers(lambda message: message.text == "Выполнить")
async def complete_task(message: types.Message, state: FSMContext):
    if bool(await data.get_tasks(tele_id=message.from_user.id, is_complete=0)):
        await bot.send_message(message.from_user.id, "Выберите задачу которую хотите пометить выполненной",
                               reply_markup=markup.choose_task(
                                   await data.get_tasks(tele_id=message.from_user.id, is_complete=0)))
        await FSM_complete_task.choose_complete.set()
    else:
        await bot.send_message(message.from_user.id, "У вас нет не законченных задач")


# @dp.callback_query_handlers(state=FSM_complete_task.choose_complete)
async def submit_complete(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != '0':
        await data.set_complete(callback_query.from_user.id, callback_query.data)
        if bool(sum(
            [int(callback_query.data == str(list(el)[0])) for el in await data.get_tasks(tele_id=callback_query.from_user.id,
                                                                                         is_complete=1)])):
            await callback_query.answer("Задача успешно отмечена выполненной")
            await bot.send_message(callback_query.from_user.id, "Успешно!")
    await callback_query.message.delete()
    await state.finish()


def register_handlers_complete_task(dp: Dispatcher):
    dp.register_message_handler(complete_task, lambda message: message.text == "Выполнить")
    dp.register_callback_query_handler(submit_complete, state=FSM_complete_task.choose_complete)