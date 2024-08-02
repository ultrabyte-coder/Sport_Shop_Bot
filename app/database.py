# Импорт необходимых модулей
import sqlite3 as sq


# Функция для инициализации базы данных
async def db_start():
    """
    Инициализирует базу данных и создает необходимые таблицы, если они отсутствуют.

    Параметры: None

    Возвращаемое значение: None
    """
    global db, cur  # Объявляем глобальные переменные для базы данных и курсора
    db = sq.connect('tg.db')  # Подключаемся к базе данных (или создаем новую)
    cur = db.cursor()  # Создаем курсор для выполнения SQL-запросов
    # Создаем таблицу accounts, если она не существует
    cur.execute('CREATE TABLE IF NOT EXISTS accounts('
                'id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'tg_id INTEGER, '
                'cart_id TEXT)')
    # Создаем таблицу items, если она не существует
    cur.execute('CREATE TABLE IF NOT EXISTS items('
                'i_id INTEGER PRIMARY KEY AUTOINCREMENT, '
                'name TEXT, '
                'desc TEXT, '
                'price TEXT, '
                'photo TEXT, '
                'brand TEXT)')
    db.commit()  # Сохраняем изменения в базе данных


async def cmd_start_db(user_id):
    """
    Создает новую запись в таблице accounts, если пользователь с указанным user_id отсутствует.

    Параметры:
        user_id: ID пользователя(целое число).

    Возвращаемое значение: None
    """
    user = cur.execute('SELECT * FROM accounts WHERE tg_id == {key}'.format(key=user_id)).fetchone()
    if not user:  # Проверяем, существует ли уже пользователь
        cur.execute('INSERT INTO accounts (tg_id) VALUES ({key})'.format(key=user_id))  # Добавляем нового пользователя
        db.commit()  # Сохраняем изменения


async def add_item(state):
    """
    Добавляет новый товар в таблицу items на основании данных из состояния state.

    Параметры:
        state: Состояние, содержащее данные о товаре(объект).

    Возвращаемое значение: None
    """
    async with state.proxy() as data:  # Получаем данные из состояния
        cur.execute('INSERT INTO items (name, desc, price, photo, brand) VALUES (?, ?, ?, ?, ?)',
                    (data['name'], data['desc'], data['price'], data['photo'], data['type']))  # Вставляем товар в базу
        db.commit()  # Сохраняем изменения


async def get_item():
    """
    Возвращает все товары из таблицы items.

    Параметры: None

    Возвращаемое значение: Список всех товаров(список кортежей).
    """
    cur.execute("SELECT * FROM items")  # Выполняем запрос для получения всех товаров
    items = cur.fetchall()  # Получаем все результаты
    return items  # Возвращаем список товаров


async def delete_item_by_id(item_id: int):
    """
    Удаляет товар из таблицы items по его ID.

    Параметры:
        item_id: ID удаляемого товара(целое число).

    Возвращаемое значение: None
    """
    cur.execute('DELETE FROM items WHERE i_id = ?', (item_id,))  # Выполняем запрос на удаление товара
    db.commit()  # Сохраняем изменения


async def get_items_by_category(category: str):
    """
    Возвращает все товары из таблицы items по указанной категории (бренду).

    Параметры:
        category: Название категории (бренд) товара (строка).

    Возвращаемое значение: Список товаров данной категории(список кортежей).
    """
    cur.execute("SELECT * FROM items WHERE brand = ?", (category,))  # Выполняем запрос для получения товаров по категории
    items = cur.fetchall()  # Получаем все результаты
    return items  # Возвращаем список товаров


async def get_item_by_id(item_id: int):
    """
    Возвращает информацию о товаре из таблицы items по его ID.

    Параметры:
        item_id: ID товара(целое число).

    Возвращаемое значение: Информация о товаре(кортеж) или None, если товар не найден.
    """
    cur.execute("SELECT * FROM items WHERE i_id = ?", (item_id,))  # Выполняем запрос для получения товара по ID
    item = cur.fetchone()  # Получаем один результат
    return item  # Возвращаем информацию


async def add_to_cart(user_id, item_id):
    """
    Добавляет товар в корзину пользователя.

    Параметры:
        user_id: ID пользователя(целое число).
        item_id: ID товара(целое число).

    Возвращаемое значение: None
    """
    # Проверяем, существует ли корзина для данного пользователя
    user_cart = cur.execute('SELECT cart_id FROM accounts WHERE tg_id = ?', (user_id,)).fetchone()
    if user_cart:
        # Если корзина существует, получаем ее ID
        cart_id = user_cart[0]
        # Добавляем товар в существующую корзину
        cur.execute('INSERT INTO cart_items (cart_id, item_id) VALUES (?, ?)', (cart_id, item_id))
        db.commit()  # Сохраняем изменения
    else:
        # Если корзины нет, создаем новую
        cur.execute('INSERT INTO cart (tg_id) VALUES (?)', (user_id,))
        cart_id = cur.lastrowid  # Получаем ID новой корзины
        # Добавляем товар в только что созданную корзину
        cur.execute('INSERT INTO cart_items (cart_id, item_id) VALUES (?, ?)', (cart_id, item_id))
        db.commit()  # Сохраняем изменения
