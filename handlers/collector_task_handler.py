from aiogram.dispatcher import Dispatcher

from handlers.task_operation.add_task_opera import register_handlers_add_task
from handlers.task_operation.complete_task_opera import register_handlers_complete_task
from handlers.task_operation.del_task_opera import register_handlers_del_task
from handlers.task_operation.open_task_opera import register_handlers_open_task
from handlers.task_operation.open_edit_menu import register_handlers_edit_task_menu
from handlers.task_operation.edit_task_opera import register_handlers_edit_task


def register_handlers_tasks(dp: Dispatcher):
    register_handlers_del_task(dp)
    register_handlers_edit_task_menu(dp)
    register_handlers_open_task(dp)
    register_handlers_add_task(dp)
    register_handlers_complete_task(dp)
    register_handlers_edit_task(dp)


