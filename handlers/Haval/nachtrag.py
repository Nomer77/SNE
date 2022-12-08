from aiogram import types
from config import bot, data
import markup
import asyncio
from aiogram.dispatcher import Dispatcher, FSMContext
from handlers.machine import FSMDashboard, FSMNachtrag
from handlers.function import delete_message, set_message_id, werkbank, umwandeln, return_dashboard, set_content_id, delete_content


async def nachtrag_description(callback_query: types.CallbackQuery, state: FSMContext):
    await FSMNachtrag.description.set()
    description = "Присылайте каждую новую задачу отдельным сообщением. Задача должна быть текстовой." \
                  "Когда пришлете все желаемые задачи, введите команду /submit \n" \
                  "Если хотите добавить к задаче время, введите его в конце задачи через пробел в формате HH:MM. \n" \
                  "Когда наступит время задачи со временим, я смогу вас оповестить. \n"
    m2u = await bot.send_message(callback_query.from_user.id, description, reply_markup=markup.button_cancel())
    await delete_message(state, callback_query.from_user.id)
    await set_message_id(state, m2u)
    await FSMNachtrag.annahme.set()

async def annahame_task(message: types.Message, state: FSMContext):
    if message.chat.id == message.from_user.id:
        accepted_tasks = await umwandeln(state, 'accepted_tasks')
        accept = {'task': (werkbank(message.text))[0], 'time': (werkbank(message.text))[1]}
        accepted_tasks.append(accept)
        async with state.proxy() as base:
            base['accepted_tasks'] = accepted_tasks


async def nachtrag_senden(message: types.Message, state: FSMContext):
    await FSMNachtrag.submit.set()
    if message.chat.id == message.from_user.id:
        accepted_tasks = await umwandeln(state, 'accepted_tasks')
        if len(accepted_tasks) < 1:
            await bot.send_message(message.from_user.id, "Действие отменено.")
            await bot.send_message(message.from_user.id, "Я не могу добавить пустую задачу", reply_markup=markup.checkout())
            await delete_message(state, message.from_user.id)
            await state.finish()
            return 0
        loading = open('gif_message/loading.mp4', 'rb')
        amount_handler = 0
        amount_accepted = 0
        rejected = []
        for task in accepted_tasks:
            amount_handler += 1
            if not await data.is_task_exists(message.from_user.id, task['task'], task['time']):
                await data.add_task(tele_id=message.from_user.id, task=task['task'], time=task['time'])
                amount_accepted += 1
            else:
                rejected.append(task)
        await asyncio.sleep(0.5)
        m2u = await bot.send_video_note(message.from_user.id, loading)
        await set_content_id(state, m2u)
        m2u = await bot.send_message(message.from_user.id, f"Добаленно {amount_accepted} задач из {amount_handler} обработанных", reply_markup=markup.button_return())
        await delete_message(state, message.from_user.id)
        await set_message_id(state, m2u)
        if amount_handler != amount_accepted:
            error_message = ''
            for task in rejected:
                if task['time'] is None:
                    error_message += f"Задача <u>{task['task']}</u> без времени - <b>уже существует</b> \n"
                else:
                    error_message += f"Задача <u>{task['task']}</u> на время <u>{task['time']}</u> - <b>уже существует</b> \n"
            await bot.send_message(message.from_user.id, error_message, parse_mode='html')





def register_nachtrag_handler(dp: Dispatcher):
    dp.register_callback_query_handler(nachtrag_description, lambda callback_query: callback_query.data == '1', state=FSMDashboard.menu)
    dp.register_message_handler(nachtrag_senden, state=FSMNachtrag.annahme, commands=['submit'])
    dp.register_message_handler(annahame_task, state=FSMNachtrag.annahme, content_types=['text'])
