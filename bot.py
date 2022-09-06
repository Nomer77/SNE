from aiogram.utils import executor
from config_bot import dp
import asyncio
from process import send_task_notification

from handlers import commands, other, collector_task_handler

commands.register_handlers_commands(dp)
collector_task_handler.register_handlers_tasks(dp)
other.register_handlers_other(dp)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(send_task_notification())
    executor.start_polling(dp, skip_updates=True)
