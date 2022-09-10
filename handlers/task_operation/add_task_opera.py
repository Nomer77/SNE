from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config_bot import bot, data
import markup
import time_manager
from handlers.task_operation.open_task_opera import open_tasks
from loguru import logger


class FSM_add_task(StatesGroup):
    adding = State()
    submit = State()


# @dp.message_handlers(lambda message: message.text == 'Добавить задачи')
async def add_task(message: types.Message):
    await bot.send_message(message.from_user.id, "Вводите задачи, каждая новая задача новым сообщением, в конце "
                                                 "сообщения введите время в формате HH:MM, если хотите добавить "
                                                 "время", reply_markup=markup.stop_adding_button())
    await FSM_add_task.adding.set()


# @dp.message_handlers(content_types=['text'], state=FSM_add_task.adding)
async def processing_task(message: types.Message, state: FSMContext):
    if message.text == "Стоп":
        await FSM_add_task.next()
        await submit_task(message, state)
    else:
        async with state.proxy() as base:
            try:
                base['amount'] += 1
            except KeyError:
                base['amount'] = 1
            base['task' + str(base['amount'])] = message.text
            await bot.send_message(message.from_user.id, f"Задача <b>{base['task' + str(base['amount'])]}</b> принята",
                                   parse_mode='html')


async def submit_task(message: types.Message, state: FSMContext):
    preven = []
    async with state.proxy() as base:
        try:
            for i in range(1, base['amount'] + 1):
                if await data.is_task_exists(message.from_user.id, base['task' + str(i)]):
                    preven.append(base['task' + str(i)])
                else:
                    await data.add_task(message.from_user.id, base['task' + str(i)],
                                        time=time_manager.find_time(base['task' + str(i)]))
            logger.info(f"User ({message.from_user.id}) {message.from_user.username} add new task")
            if bool(len(preven)):
                for el in preven:
                    await bot.send_message(message.from_user.id, f"Задача '{el}' уже существует и не была добавлена "
                                                                 f"повторно")
                logger.info(f"User ({message.from_user.id}) {message.from_user.username} try add existing task")
        except KeyError:
            pass
    await state.finish()
    await open_tasks(message)


def register_handlers_add_task(dp: Dispatcher):
    dp.register_message_handler(add_task, lambda message: message.text == 'Добавить задачи')
    dp.register_message_handler(processing_task, content_types=['text'], state=FSM_add_task.adding)
