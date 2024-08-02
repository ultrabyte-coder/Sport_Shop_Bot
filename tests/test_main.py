import os
import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from unittest import IsolatedAsyncioTestCase

from main import on_startup


class TestBot(IsolatedAsyncioTestCase):
    """Тесты для проверки функциональности бота."""

    @patch.dict(os.environ, {'TOKEN': 'test_token_value'})
    async def asyncSetUp(self):
        """
        Настройка окружения перед выполнением тестов.

        - Загружает переменные окружения из .env файла.
        - Создает экземпляр хранилища для хранения состояния бота.
        - Создает мок-объект для бота и устанавливает его токен.
        - Инициализирует диспетчер с созданным ботом и хранилищем.
        """
        load_dotenv()

        # Создаем экземпляр хранилища и бота
        self.storage = MemoryStorage()
        self.bot = MagicMock(spec=Bot)  # Используем мок вместо реального экземпляра
        self.bot.token = 'test_token_value'  # Устанавливаем атрибут token
        self.dp = Dispatcher(bot=self.bot, storage=self.storage)

    @patch('app.database.db_start', new_callable=AsyncMock)
    async def test_on_startup(self, mock_db_start):
        """
        Тестирует функцию on_startup.

        Проверяет, что функция db_start вызывается один раз при запуске бота.

        Аргументы:
            mock_db_start (AsyncMock): Мок для функции db_start,
            чтобы проверить ее вызов.
        """
        await on_startup(None)  # Передаем None, если не используется
        mock_db_start.assert_called_once()

    async def test_bot_instance(self):
        """
        Тестирует экземпляр бота.

        Проверяет, что создаваемый объект бота является экземпляром
        MagicMock и имеет правильный токен.
        """
        # Проверяем, что тип self.bot - это MagicMock
        self.assertIsInstance(self.bot, MagicMock)
        # Сравниваем токен с ожидаемым значением
        self.assertEqual(self.bot.token, 'test_token_value')

    async def test_dispatcher_instance(self):
        """
        Тестирует экземпляр диспетчера.

        Проверяет, что диспетчер инициализируется правильно с
        заданным ботом и хранилищем.
        """
        # Проверяем экземпляры диспетчера
        self.assertIsInstance(self.dp, Dispatcher)
        self.assertEqual(self.dp.bot, self.bot)
        self.assertEqual(self.dp.storage, self.storage)


# Запуск тестов
if __name__ == '__main__':
    unittest.main()





