from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config_bot import bot, dp, data
import markup
import time_manager


async def open_tasks(message: types.Message):
    if bool(await data.get_tasks(tele_id=message.from_user.id)):
        await bot.send_message(message.from_user.id, "Вот ваши задачи", reply_markup=markup.task_button())
        amount = 0
        for value in await data.get_tasks(tele_id=message.from_user.id, is_complete=0):
            amount += 1
            await bot.send_message(message.from_user.id, f"{amount}. {value[0]}")
        for value in await data.get_tasks(tele_id=message.from_user.id, is_complete=1):
            amount += 1
            await bot.send_message(message.from_user.id, f"<s>{amount}. <i>{value[0]}</i></s>", parse_mode='html')
    else:
        await bot.send_message(message.from_user.id, "У вас нету задач :(", reply_markup=markup.task_button())


""" Выполнить задачу """


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


"""" Добавление задачи """


class FSM_add_task(StatesGroup):
    adding = State()
    submit = State()


# @dp.message_handlers(lambda message: message.text == 'Добавить задачи')
async def add_task(message: types.Message):
    await bot.send_message(message.from_user.id, "Something: ", reply_markup=markup.stop_adding_button())
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
    async with state.proxy() as base:
        try:
            for i in range(1, base['amount'] + 1):
                await data.add_task(message.from_user.id, base['task' + str(i)],
                                    time=time_manager.find_time(base['task' + str(i)]))
        except KeyError:
            pass
    await state.finish()
    await open_tasks(message)


"""" Редактировать """


# @dp.message_handler(lambda message: message.text == "Редактировать")
async def edit_task(message: types.Message):
    await bot.send_message(message.from_user.id, "Ыгы", reply_markup=markup.edit_task_button())


""" Удалить задачу """


class FSM_delete_task(StatesGroup):
    choose_delete = State()


# @dp.message_handlers(lambda message: message.text == "Удалить задачу")
async def delete_task(message: types.Message, state: FSMContext):
    if bool(await data.get_tasks(message.from_user.id)):
        await bot.send_message(message.from_user.id, "Выберите задачу которую хотите удалить",
                               reply_markup=markup.choose_task(await data.get_tasks(message.from_user.id)))
        await FSM_delete_task.choose_delete.set()
    else:
        await bot.send_message(message.from_user.id, "У вас нет задач :(")


# @dp.callback_query_handlers(state=FSM_delete_task.choose_delete)
async def submit_delete(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data != '0':
        await data.delete_task(callback_query.from_user.id, callback_query.data)
        if not bool(sum([int(callback_query.data in el) for el in await data.get_tasks(callback_query.from_user.id)])):
            await callback_query.answer("Задача успешно удалена!")
            await bot.send_message(callback_query.from_user.id, "Успешно!")
    await callback_query.message.delete()
    await state.finish()


def register_handlers_tasks(dp: Dispatcher):
    dp.register_message_handler(open_tasks, lambda message: message.text == 'Задачи')
    dp.register_message_handler(add_task, lambda message: message.text == 'Добавить задачи')
    dp.register_message_handler(processing_task, content_types=['text'], state=FSM_add_task.adding)
    dp.register_message_handler(complete_task, lambda message: message.text == "Выполнить")
    dp.register_callback_query_handler(submit_complete, state=FSM_complete_task.choose_complete)
    dp.register_message_handler(edit_task, lambda message: message.text == "Редактировать")
    dp.register_message_handler(delete_task, lambda message: message.text == "Удалить задачу")
    dp.register_callback_query_handler(submit_delete, state=FSM_delete_task.choose_delete)
