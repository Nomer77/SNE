from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from DataBase import db
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token='5381866137:AAFVSI579I4Co-qj8-wiqY_QdhFUSVselFQ')
dp = Dispatcher(bot, storage=storage)
data = db.TeleData('DataBase/server.db')

# JSON

menu_buttons = ['Персонализация', 'Список задач 📃', 'Обратная связь 📬']
dashboard_buttons = ['Получить список задач 📃', 'Добавить задачи 📝', 'Выполнить задачу ✅', 'Изменить задачу ✏️', 'Удалить задачу  ❌']
service_buttons = ['Курсы валют 💵']
