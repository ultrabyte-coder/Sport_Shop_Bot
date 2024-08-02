# Импорт необходимых модулей
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


# Создание экземпляра ReplyKeyboardMarkup для основного меню
main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('КАТАЛОГ').add('КОРЗИНА').add('КОНТАКТЫ')

# Создание экземпляра ReplyKeyboardMarkup для основного меню администратора
main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('КАТАЛОГ').add('КОРЗИНА').add('КОНТАКТЫ').add('Админ-панель')

# Создание экземпляра ReplyKeyboardMarkup для админ-панели
admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Показать товары')


# Функция для создания кнопки "Добавить в корзину"
def create_add_to_cart_button(item_id):
    """
    Создает кнопку "Добавить в корзину" для указанного товара.

    Args:
        item_id (int): Идентификатор товара.

    Returns:
        InlineKeyboardButton: Кнопка "Добавить в корзину".
    """
    return InlineKeyboardButton("Добавить в корзину", callback_data=f"add_to_cart_{item_id}")


# Функция для создания клавиатуры с кнопкой "Добавить в корзину"
def create_keyboard_with_add_to_cart_button(item_id):
    """
    Создает клавиатуру с кнопкой "Добавить в корзину" для указанного товара.

    Args:
        item_id (int): Идентификатор товара.

    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопкой "Добавить в корзину".
    """
    add_button = create_add_to_cart_button(item_id)
    keyboard = InlineKeyboardMarkup().add(add_button)
    return keyboard


# Функция для создания кнопки "Удалить [название товара]"
def create_remove_from_cart_button(item_id, item_name):
    """
    Создает кнопку "Удалить [название товара]" для указанного товара.

    Args:
        item_id (int): Идентификатор товара.
        item_name (str): Название товара.

    Returns:
        InlineKeyboardButton: Кнопка "Удалить [название товара]".
    """
    return InlineKeyboardButton(f"Удалить {item_name}", callback_data=f"remove_from_cart_{item_id}")


# Функция для создания кнопки "Оформить заказ"
def create_place_order_button():
    """
    Создает кнопку "Оформить заказ".

    Returns:
        InlineKeyboardButton: Кнопка "Оформить заказ".
    """
    return InlineKeyboardButton("Оформить заказ", callback_data="place_order")


# Функция для создания кнопки "Удалить" и клавиатуры с этой кнопкой
def create_delete_item_button(item_id):
    """
    Создает кнопку "Удалить" и клавиатуру с этой кнопкой для указанного товара.

    Args:
        item_id (int): Идентификатор товара.

    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопкой "Удалить".
    """
    delete_button = InlineKeyboardButton("Удалить", callback_data=f"delete_item_{item_id}")
    keyboard = InlineKeyboardMarkup().add(delete_button)
    return keyboard


# Создание экземпляра InlineKeyboardMarkup для списка категорий каталога
catalog_list = InlineKeyboardMarkup(row_width=2)
catalog_list.add(InlineKeyboardButton(text='Футболки', callback_data='t-shirt'),
                 InlineKeyboardButton(text='Кроссовки', callback_data='sneakers'),
                 InlineKeyboardButton(text='Толстовки', callback_data='hoodies'),
                 InlineKeyboardButton(text='Спортивные костюмы', callback_data='tracksuits'),
                 InlineKeyboardButton(text='Шорты', callback_data='shorts'),
                 InlineKeyboardButton(text='Куртки', callback_data='jackets'))

# Создание экземпляра ReplyKeyboardMarkup для отмены операции
cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add('ОТМЕНА')


