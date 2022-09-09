from aiogram.utils import executor
from config_bot import dp
import asyncio
from process import checking_time
from loguru import logger

from handlers import commands, other, collector_task_handler

logger.add("logs/log_file.log", format="{time} | {level} | {message}", level="INFO", rotation='25 KB', compression="zip")

commands.register_handlers_commands(dp)
collector_task_handler.register_handlers_tasks(dp)
other.register_handlers_other(dp)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(checking_time())
    executor.start_polling(dp, skip_updates=True)
