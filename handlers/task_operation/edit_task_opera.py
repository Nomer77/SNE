from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher, FSMContext
from handlers.task_operation.open_task_opera import open_tasks
from aiogram import types
from config_bot import bot, data
import markup
import time_manager
from loguru import logger


class FSM_edit_task(StatesGroup):
    choose_task = State()
    submit_task = State()


# @dp.message_handler(lambda message: message.text == 'Редактировать задачу')
async def choose_edit_task(message: types.Message):
    if bool(await data.get_tasks(message.from_user.id, is_complete=0)):
        await bot.send_message(message.from_user.id, "Выберите задачу которую хотите отредактировать",
                               reply_markup=await markup.choose_task(
                                await data.get_tasks(message.from_user.id, is_complete=0), message.from_user.id))
        await FSM_edit_task.choose_task.set()
    else:
        await bot.send_message(message.from_user.id, "У вас нет задач :(")


# @dp.message_handler(state=FSM_edit_task.choose_task)
async def edit_task(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    if callback_query.data != '0':
        task = await data.get_tasks(callback_query.from_user.id, task_id=callback_query.data)
        await bot.send_message(callback_query.from_user.id, "Введите измененную задачу: ")
        await FSM_edit_task.next()
        async with state.proxy() as base:
            base['query'] = task[0][0]
    else:
        await bot.send_message(callback_query.from_user.id, "Принято", reply_markup=markup.edit_task_button())
        await state.finish()


# @dp.message_handler(state=FSM_edit_task.submit_task)
async def submit_edit_task(message: types.Message, state: FSMContext):
    async with state.proxy() as base:
        task = base['query']
    task_id = await data.get_task_id(message.from_user.id, task)
    await data.update_task(message.from_user.id, task, message.text, time=time_manager.find_time(message.text))
    edited = await data.get_tasks(tele_id=message.from_user.id, task_id=task_id)
    if edited[0][0] == message.text:
        await bot.send_message(message.from_user.id, "Готово", reply_markup=markup.edit_task_button())
        await open_tasks(message)
        logger.info(f"User ({message.from_user.id}) {message.from_user.username} edited task")
    await state.finish()


def register_handlers_edit_task(dp: Dispatcher):
    dp.register_message_handler(choose_edit_task, lambda message: message.text == 'Редактировать задачу')
    dp.register_callback_query_handler(edit_task, state=FSM_edit_task.choose_task)
    dp.register_message_handler(submit_edit_task, state=FSM_edit_task.submit_task)