from aiogram import types
from config import bot, data
import markup
import asyncio
from aiogram.dispatcher import Dispatcher, FSMContext
from handlers.machine import FSMBoard, FSMValute
from handlers.function import delete_message, set_message_id, set_content_id, delete_content


async def valute_auswalh(callback_query: types.CallbackQuery, state: FSMContext):
    await FSMValute.auswalh.set()
    description = "=== Центр валют === \n" \
    "Здесь вы можете подписаться/отписаться на рассылку курс валют, каждый день с утра при обновлением задач \n"
    status = await data.get_valute_status(callback_query.from_user.id)
    button = (lambda int_status: 'Отписаться ❌' if bool(int_status) else 'Подписаться ✅')(status)
    m2u = await bot.send_message(callback_query.from_user.id, description, reply_markup=markup.buttons_list_return([button]))
    await delete_message(state, callback_query.from_user.id)
    await set_message_id(state, m2u)
    await FSMValute.submit.set()

async def valute_submit(callback_query: types.CallbackQuery, state: FSMContext):
    valute = open('gif_message/valute.mp4', 'rb')
    await data.valute_transform(callback_query.from_user.id, abs(await data.get_valute_status(callback_query.from_user.id) - 1))
    if bool(await data.get_valute_status(callback_query.from_user.id)):
        await asyncio.sleep(0.5)
        m2u = await bot.send_video_note(callback_query.from_user.id, valute)
        await set_content_id(state, m2u)
    m2u = await bot.send_message(callback_query.from_user.id, f"Изменения успешно внесены!", reply_markup=markup.buttons_list_return([]))
    await delete_message(state, callback_query.from_user.id)
    await set_message_id(state, m2u)


def register_currencies_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(valute_auswalh, lambda callback_query: callback_query.data == '0', state=FSMBoard.menu)
    dp.register_callback_query_handler(valute_submit, state=FSMValute.submit)