from aiogram.utils import executor
from config import dp
import asyncio
from process import checking_time

from handlers.commands import register_handlers_commands
from handlers.abrogate import register_abrogate_handler
from handlers.Haval.dashboard import register_dashboard_handler
from handlers.Haval.nachtrag import register_nachtrag_handler
from handlers.Haval.complete import register_complete_handler
from handlers.Haval.zeigen import register_zeigen_handler
from handlers.Haval.delete import register_delete_handler
from handlers.Haval.edit import register_edit_handler
from handlers.feedback import register_handlers_feedback
from handlers.other import register_handlers_other
from handlers.Subaru.board import register_board_handlers
from handlers.Subaru.currencies import register_currencies_handlers


register_handlers_commands(dp)
register_handlers_other(dp)
register_abrogate_handler(dp)
register_dashboard_handler(dp)
register_zeigen_handler(dp)
register_nachtrag_handler(dp)
register_complete_handler(dp)
register_delete_handler(dp)
register_edit_handler(dp)
register_handlers_feedback(dp)
register_board_handlers(dp)
register_currencies_handlers(dp)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(checking_time())
    executor.start_polling(dp, skip_updates=True)