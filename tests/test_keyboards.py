import unittest
from app.keyboards import main, main_admin, admin_panel, create_add_to_cart_button, create_keyboard_with_add_to_cart_button, create_remove_from_cart_button, create_place_order_button, create_delete_item_button, catalog_list, cancel
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


class TestKeyboards(unittest.TestCase):
    """Тесты для проверки корректности работы клавиатур бота."""

    def test_main_keyboard(self):
        """Проверяет основную клавиатуру бота."""
        self.assertIsInstance(main, ReplyKeyboardMarkup)
        buttons_count = sum(len(row) for row in main.keyboard)
        self.assertEqual(buttons_count, 3)

    def test_main_admin_keyboard(self):
        """Проверяет административную клавиатуру бота."""
        self.assertIsInstance(main_admin, ReplyKeyboardMarkup)
        buttons_count = sum(len(row) for row in main_admin.keyboard)
        self.assertEqual(buttons_count, 4)

    def test_admin_panel_keyboard(self):
        """Проверяет панель администратора."""
        self.assertIsInstance(admin_panel, ReplyKeyboardMarkup)
        buttons_count = sum(len(row) for row in admin_panel.keyboard)
        self.assertEqual(buttons_count, 2)

    def test_create_add_to_cart_button(self):
        """Проверяет создание кнопки 'Добавить в корзину'."""
        button = create_add_to_cart_button(1)
        self.assertIsInstance(button, InlineKeyboardButton)
        self.assertEqual(button.text, "Добавить в корзину")
        self.assertEqual(button.callback_data, "add_to_cart_1")

    def test_create_keyboard_with_add_to_cart_button(self):
        """Проверяет создание клавиатуры с одной кнопкой 'Добавить в корзину'."""
        keyboard = create_keyboard_with_add_to_cart_button(1)
        self.assertIsInstance(keyboard, InlineKeyboardMarkup)
        self.assertEqual(len(keyboard.inline_keyboard), 1)
        self.assertEqual(len(keyboard.inline_keyboard[0]), 1)

    def test_create_remove_from_cart_button(self):
        """Проверяет создание кнопки 'Удалить товар'."""
        button = create_remove_from_cart_button(1, "Товар")
        self.assertIsInstance(button, InlineKeyboardButton)
        self.assertEqual(button.text, "Удалить Товар")
        self.assertEqual(button.callback_data, "remove_from_cart_1")

    def test_create_place_order_button(self):
        """Проверяет создание кнопки 'Оформить заказ'."""
        button = create_place_order_button()
        self.assertIsInstance(button, InlineKeyboardButton)
        self.assertEqual(button.text, "Оформить заказ")
        self.assertEqual(button.callback_data, "place_order")

    def test_create_delete_item_button(self):
        """Проверяет создание клавиатуры для удаления товара."""
        keyboard = create_delete_item_button(1)
        self.assertIsInstance(keyboard, InlineKeyboardMarkup)
        self.assertEqual(len(keyboard.inline_keyboard), 1)
        self.assertEqual(len(keyboard.inline_keyboard[0]), 1)

    def test_catalog_list_keyboard(self):
        """Проверяет клавиатуру каталога товаров."""
        self.assertIsInstance(catalog_list, InlineKeyboardMarkup)
        buttons_count = sum(len(row) for row in catalog_list.inline_keyboard)
        self.assertEqual(buttons_count, 6)

    def test_cancel_keyboard(self):
        """Проверяет клавиатуру отмены действия."""
        self.assertIsInstance(cancel, ReplyKeyboardMarkup)
        buttons_count = sum(len(row) for row in cancel.keyboard)
        self.assertEqual(buttons_count, 1)


#  Запуск тестов
if __name__ == '__main__':
    unittest.main()