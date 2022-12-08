import asyncio
import datetime
from config import data, bot
import pycbrf


async def checking_time():
    while True:
        time = f"{datetime.datetime.now().hour}:{'{:02}'.format(datetime.datetime.now().minute)}"
        z_time = f"{'{:02}'.format(datetime.datetime.now().hour)}:{'{:02}'.format(datetime.datetime.now().minute)}"
        if bool(await data.get_tasks(is_complete=0, time=time)):
            for value in await data.get_tasks(is_complete=0, time=time):
                chat_id = await data.get_task_owner(value[0])
                await bot.send_message(chat_id[0], f"Пришло время выполнить задачу <u>{value[1]}</u> на время <u>{value[2]}</u>", parse_mode='html')
        if bool(await data.get_tasks(is_complete=0, time=z_time)) and (datetime.datetime.now().hour) < 10:
            for value in await data.get_tasks(is_complete=0, time=z_time):
                chat_id = await data.get_task_owner(value[0])
                await bot.send_message(chat_id[0], f"Пришло время выполнить задачу <u>{value[1]}</u> на время <u>{value[2]}</u>", parse_mode='html')

        if time == "8:00":
            await data.delete_all_task()
            rates = pycbrf.ExchangeRates('2022-12-07')
            for user in await data.get_users():
                await bot.send_message(user[0], "Доброе утро! Все ваши задачи сброшены. Пора приступить к "
                                                "планированию задач на день!", parse_mode='html')
                if await bool(await data.get_valute_status(user[0])):
                    await bot.send_message(user[0], f"1 {rates['USD'].name} = {rates['USD'].rate} Российских рублей")

        if time == "22:00":
            for user in await data.get_users():
                all_tasks = await data.get_tasks(tele_id=user[0])
                cmp_tasks = await data.get_tasks(tele_id=user[0], is_complete=1)
                if bool(await data.get_tasks(tele_id=user[0])):
                    await bot.send_message(user[0], f"День подходит к концу и за него вы успели выполнить "
                                                    f"<b>{len(cmp_tasks)} из {len(all_tasks)}</b> задач! Доброй ночи! ",
                                           parse_mode='html')
                else:
                    await bot.send_message(user[0], f"К сожалению вы сегодня ничего не планировали. Завтра надо всё "
                                                    f"наверстать! Доброй ночи!")
        await asyncio.sleep(60)
