from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher, FSMContext
from config_bot import bot, data
import markup
from loguru import logger


class FSM_complete_task(StatesGroup):
    choose_complete = State()


# @dp.message_handlers(lambda message: message.text == "Выполнить")
async def complete_task(message: types.Message, state: FSMContext):
    if bool(await data.get_tasks(tele_id=message.from_user.id, is_complete=0)):
        await bot.send_message(message.from_user.id, "Выберите задачу которую хотите пометить выполненной",
                               reply_markup=await markup.choose_task(
                                   await data.get_tasks(tele_id=message.from_user.id, is_complete=0),
                                   message.from_user.id))
        await FSM_complete_task.choose_complete.set()
    else:
        await bot.send_message(message.from_user.id, "У вас нет не законченных задач")


# @dp.callback_query_handlers(state=FSM_complete_task.choose_complete)
async def submit_complete(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != '0':
        task = await data.get_tasks(callback_query.from_user.id, task_id=callback_query.data)
        await data.set_complete(callback_query.from_user.id, task[0][0])
        if bool(sum(
                [int(task[0][0] == str(list(el)[0])) for el in await data.get_tasks(tele_id=callback_query.from_user.id,
                                                                                    is_complete=1)])):
            await callback_query.answer("Задача успешно отмечена выполненной")
            await bot.send_message(callback_query.from_user.id, "Успешно!")
            logger.info(
                f"User ({callback_query.from_user.id}) {callback_query.from_user.username} completed '{task[0][0]}'")
    await callback_query.message.delete()
    await state.finish()


def register_handlers_complete_task(dp: Dispatcher):
    dp.register_message_handler(complete_task, lambda message: message.text == "Выполнить")
    dp.register_callback_query_handler(submit_complete, state=FSM_complete_task.choose_complete)
