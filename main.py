# Импорт необходимых модулей
import os
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

# Создание экземпляра MemoryStorage для хранения данных состояний
storage = MemoryStorage()

# Загрузка переменных среды из файла .env
load_dotenv()

# Создание экземпляра бота, используя токен из переменной среды
bot = Bot(os.getenv('TOKEN'))

# Создание диспетчера с указанием бота и хранилища
dp = Dispatcher(bot=bot, storage=storage)


# Функция, вызываемая при запуске бота
async def on_startup(_):
    """
    Функция, вызываемая при запуске бота.

    Args:
        _ (Any): Аргумент, который не используется в функции.

    Returns:
        None
    """
    await db.db_start()  # Начало работы с базой данных
    print('Бот успешно запущен!')

# Импорт всех обработчиков из пакета app.handlers
from app.handlers import *

# Запуск бота
if __name__ == '__main__':
    # Запуск бота с указанием функции on_startup для выполнения действий при старте
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
