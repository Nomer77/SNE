import asyncio
import time_manager
from config_bot import data, bot
from loguru import logger


async def checking_time():
    while True:
        time = time_manager.now_sec_time()
        if bool(await data.get_tasks(is_complete=0, time=time)):
            for value in await data.get_tasks(is_complete=0, time=time):
                for user in await data.get_task_user(value[0], time):
                    await bot.send_message(user[0], f"Пришло время выполнить задачу '{value[0]}'")
                    logger.info(f"Bot send reminder to user {user[0]}")

        if time == (8 * 3600):
            await data.delete_task()
            for user in await data.get_users():
                await bot.send_message(user[0], "Доброе утро! Все ваши задачи сброшены. Пора приступить к "
                                                "планированию задач на день!", parse_mode='html')
            logger.info("Happy new day!")

        if time == (22 * 3600):
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
            logger.info("Bot send message about end of day")
        await asyncio.sleep(60)
