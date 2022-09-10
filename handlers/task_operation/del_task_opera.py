from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config_bot import bot, data
import markup
from loguru import logger


class FSM_delete_task(StatesGroup):
    choose_delete = State()


# @dp.message_handlers(lambda message: message.text == "Удалить задачу")
async def delete_task(message: types.Message, state: FSMContext):
    if bool(await data.get_tasks(message.from_user.id)):
        await bot.send_message(message.from_user.id, "Выберите задачу которую хотите удалить",
                               reply_markup=await markup.choose_task(await data.get_tasks(message.from_user.id),
                                                                     message.from_user.id))
        await FSM_delete_task.choose_delete.set()
    else:
        await bot.send_message(message.from_user.id, "У вас нет задач :(")


# @dp.callback_query_handlers(state=FSM_delete_task.choose_delete)
async def submit_delete(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != '0':
        task = await data.get_tasks(callback_query.from_user.id, task_id=callback_query.data)
        await data.delete_task(tele_id=callback_query.from_user.id, task=task[0][0])
        if not bool(sum([int(task[0][0] in el) for el in await data.get_tasks(callback_query.from_user.id)])):
            await callback_query.answer("Задача успешно удалена!")
            await bot.send_message(callback_query.from_user.id, "Успешно!")
            logger.info(f"User ({callback_query.from_user.id}) {callback_query.from_user.username} deleted '{task[0][0]}'")
    await callback_query.message.delete()
    await state.finish()


def register_handlers_del_task(dp: Dispatcher):
    dp.register_message_handler(delete_task, lambda message: message.text == "Удалить задачу")
    dp.register_callback_query_handler(submit_delete, state=FSM_delete_task.choose_delete)