import asyncio
import time_manager
from config_bot import data, bot


async def send_task_notification():
    while True:
        time = time_manager.now_sec_time()
        if bool(await data.get_tasks(is_complete=0, time=time)):
            for value in await data.get_tasks(is_complete=0, time=time):
                for user in await data.get_task_user(value[0], time):
                    await bot.send_message(user[0], f"Пришло время выполнить задачу '{value[0]}'")
        await asyncio.sleep(60)
