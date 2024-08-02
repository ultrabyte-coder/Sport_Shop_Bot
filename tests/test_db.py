import aiosqlite
import unittest


class TestDatabase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Создаем временную базу данных для тестов."""
        # Подключаемся к памяти (in-memory) для создания временной базы данных
        self.db = await aiosqlite.connect(':memory:')
        self.cur = await self.db.cursor()

        # Создаем таблицы для тестирования
        await self.cur.execute('CREATE TABLE IF NOT EXISTS accounts('
                               'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                               'tg_id INTEGER, '
                               'cart_id TEXT)')
        await self.cur.execute('CREATE TABLE IF NOT EXISTS items('
                               'i_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                               'name TEXT, '
                               'desc TEXT, '
                               'price TEXT, '
                               'photo TEXT, '
                               'brand TEXT)')
        await self.cur.execute('CREATE TABLE IF NOT EXISTS cart('
                               'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                               'tg_id INTEGER)')
        await self.cur.execute('CREATE TABLE IF NOT EXISTS cart_items('
                               'cart_id INTEGER, '
                               'item_id INTEGER)')
        await self.db.commit()  # Сохраняем изменения

    async def asyncTearDown(self):
        """Закрываем соединение с базой данных после тестов."""
        await self.cur.close()
        await self.db.close()

    async def test_cmd_start_db(self):
        """Тестируем добавление нового пользователя в таблицу accounts."""
        user_id = 12345  # Задаем идентификатор пользователя
        await self.cur.execute('INSERT INTO accounts (tg_id) VALUES (?)', (user_id,))
        await self.db.commit()  # Сохраняем изменения

        # Пытаемся извлечь пользователя из базы данных по tg_id
        result = await self.cur.execute('SELECT * FROM accounts WHERE tg_id = ?', (user_id,))
        user = await result.fetchone()  # Получаем данные о пользователе

        # Получаем данные о пользователе
        self.assertIsNotNone(user)
        self.assertEqual(user[1], user_id)  # Проверяем правильность tg_id

    async def test_add_item(self):
        """Тестируем добавление товара в таблицу items."""
        item_data = {
            'name': 'Test Item',
            'desc': 'This is a test item.',
            'price': '9.99',
            'photo': 'http://example.com/photo.jpg',
            'brand': 'Test Brand'
        }

        # Добавляем товар в таблицу items
        await self.cur.execute('INSERT INTO items (name, desc, price, photo, brand) VALUES (?, ?, ?, ?, ?)',
                               (item_data['name'], item_data['desc'], item_data['price'],
                                item_data['photo'], item_data['brand']))
        await self.db.commit()  # Сохраняем изменения

        # Проверяем, что товар был добавлен
        result = await self.cur.execute("SELECT * FROM items WHERE name = ?", (item_data['name'],))
        item = await result.fetchone()

        # Убеждаемся, что товар существует и поля совпадают
        self.assertIsNotNone(item)
        self.assertEqual(item[1], item_data['name'])  # Проверяем имя товара
        self.assertEqual(item[2], item_data['desc'])  # Проверяем описание товара

    async def test_get_items_by_category(self):
        """Тестируем получение товаров по категории (бренду)."""
        # Добавляем несколько товаров разных брендов
        await self.cur.execute('INSERT INTO items (name, desc, price, photo, brand) VALUES (?, ?, ?, ?, ?)',
                               ('Item A', 'Description A', '10', 'http://example.com/a.jpg', 'Brand1'))
        await self.cur.execute('INSERT INTO items (name, desc, price, photo, brand) VALUES (?, ?, ?, ?, ?)',
                               ('Item B', 'Description B', '20', 'http://example.com/b.jpg', 'Brand2'))
        await self.cur.execute('INSERT INTO items (name, desc, price, photo, brand) VALUES (?, ?, ?, ?, ?)',
                               ('Item C', 'Description C', '30', 'http://example.com/c.jpg', 'Brand1'))
        await self.db.commit()  # Сохраняем изменения

        # Извлекаем товары по бренду Brand1
        items = await self.cur.execute("SELECT * FROM items WHERE brand = ?", ('Brand1',))
        items_list = await items.fetchall()  # Получаем список товаров

        self.assertEqual(len(items_list), 2)  # Ожидаем, что будет 2 товара от Brand1

    async def test_get_item_by_id(self):
        # Тестируем получение товара по ID
        await self.cur.execute('INSERT INTO items (name, desc, price, photo, brand) VALUES (?, ?, ?, ?, ?)',
                               ('Item D', 'Description D', '40', 'http://example.com/d.jpg', 'Brand3'))
        await self.db.commit()

        result = await self.cur.execute("SELECT * FROM items WHERE i_id = 1")  # Получаем первый элемент
        item = await result.fetchone()

        self.assertIsNotNone(item)
        self.assertEqual(item[1], 'Item D')

    async def test_delete_item_by_id(self):
        # Тестируем удаление товара по ID
        await self.cur.execute('INSERT INTO items (name, desc, price, photo, brand) VALUES (?, ?, ?, ?, ?)',
                               ('Item E', 'Description E', '50', 'http://example.com/e.jpg', 'Brand4'))
        await self.db.commit()

        # Получаем ID последнего добавленного элемента
        last_item_result = await self.cur.execute("SELECT i_id FROM items WHERE name = ?", ('Item E',))
        last_item = await last_item_result.fetchone()
        item_id_to_delete = last_item[0]

        # Удаляем элемент
        await self.cur.execute("DELETE FROM items WHERE i_id = ?", (item_id_to_delete,))
        await self.db.commit()

        # Проверяем, что элемент был удален
        result = await self.cur.execute("SELECT * FROM items WHERE i_id = ?", (item_id_to_delete,))
        deleted_item = await result.fetchone()

        self.assertIsNone(deleted_item)

    async def test_add_to_cart(self):
        # Тестируем добавление товара в корзину
        user_id = 12345
        await self.cur.execute('INSERT INTO accounts (tg_id) VALUES (?)', (user_id,))
        await self.db.commit()

        # Добавляем товар для тестирования
        await self.cur.execute('INSERT INTO items (name, desc, price, photo, brand) VALUES (?, ?, ?, ?, ?)',
                               ('Test Item', 'This is a test item.', '19.99', 'http://example.com/test.jpg',
                                'Test Brand'))
        await self.db.commit()

        # Получаем ID добавленного товара
        result = await self.cur.execute("SELECT i_id FROM items WHERE name = ?", ('Test Item',))
        item = await result.fetchone()
        item_id = item[0]

        # Симулируем выполнение функции add_to_cart
        result = await self.cur.execute('SELECT cart_id FROM accounts WHERE tg_id = ?', (user_id,))
        user_cart = await result.fetchone()
        if user_cart and user_cart[0]:
            cart_id = user_cart[0]
            await self.cur.execute('INSERT INTO cart_items (cart_id, item_id) VALUES (?, ?)', (cart_id, item_id))
        else:
            await self.cur.execute('INSERT INTO cart (tg_id) VALUES (?)', (user_id,))
            cart_id = self.cur.lastrowid
            await self.cur.execute('INSERT INTO cart_items (cart_id, item_id) VALUES (?, ?)', (cart_id, item_id))
            await self.cur.execute('UPDATE accounts SET cart_id = ? WHERE tg_id = ?', (cart_id, user_id))
        await self.db.commit()

        # Проверяем, что товар был добавлен в корзину
        result = await self.cur.execute('SELECT * FROM cart_items WHERE cart_id = ? AND item_id = ?',
                                        (cart_id, item_id))
        cart_item = await result.fetchone()

        self.assertIsNotNone(cart_item)
        self.assertEqual(cart_item[0], cart_id)
        self.assertEqual(cart_item[1], item_id)

        # Проверяем, что у пользователя обновился cart_id
        result = await self.cur.execute('SELECT cart_id FROM accounts WHERE tg_id = ?', (user_id,))
        updated_user = await result.fetchone()

        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user[0], str(cart_id))

        # Проверяем, что товар существует
        result = await self.cur.execute('SELECT * FROM items WHERE i_id = ?', (item_id,))
        item = await result.fetchone()

        self.assertIsNotNone(item)
        self.assertEqual(item[1], 'Test Item')  # Проверяем имя товара


# Запуск тестов
if __name__ == '__main__':
    unittest.main()





