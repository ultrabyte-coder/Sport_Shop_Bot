import os
from unittest.mock import AsyncMock
import pytest
from app.handlers import cmd_start, catalog
from app import keyboards as kb


# Фикстура для настройки переменной окружения USER_ID
@pytest.fixture
def user_id_env():
    os.environ['USER_ID'] = '12345'
    yield
    del os.environ['USER_ID']


@pytest.mark.asyncio
async def test_cmd_start_admin(mocker):
    """
    Тестирует обработчик команды /start для администраторов.

    Проверяет, что:
    1. Функция cmd_start_db вызывается с корректным идентификатором администратора.
    2. Отправка стикера и двух сообщений выполняется правильно.
    """
    user_id = int(os.getenv('ADMIN_ID'))  # ID администратора из переменной окружения
    user_name = 'AdminUser'

    mock_message = AsyncMock()
    mock_message.from_user.id = user_id
    mock_message.from_user.first_name = user_name

    # Моки для методов message
    mock_message.answer_sticker = AsyncMock()
    mock_message.answer = AsyncMock()

    # Мокирование вызова к базе данных
    mock_cmd_start_db = mocker.patch('app.database.cmd_start_db',
                                     return_value=None)

    await cmd_start(mock_message)

    # Проверяем, что функция cmd_start_db была вызвана
    mock_cmd_start_db.assert_called_once_with(user_id)

    # Проверяем, что стикер был отправлен
    mock_message.answer_sticker.assert_called_once_with(
        'CAACAgIAAxkBAAMUZbtK1xhqVemnfFwQDUAUAR1wyUUAAo4PAAINxghKa4BZohcI5Jc0BA'
    )

    # Проверяем, что первое сообщение отправлено с правильным текстом и клавиатурой
    mock_message.answer.assert_any_call(
        f'{user_name}, добро пожаловать в спортивный магазин Sport Shop!',
        reply_markup=kb.main
    )

    # Проверяем, что второе сообщение для администратора также было отправлено
    mock_message.answer.assert_any_call(
        'ВЫ АВТОРИЗОВАЛИСЬ КАК АДМИНИСТРАТОР!',
        reply_markup=kb.main_admin
    )


@pytest.mark.asyncio
async def test_catalog_handler(mocker, user_id_env):
    """
    Тестирует обработчик каталога товаров.

    Проверяет, что пользователь получает сообщение с предложением выбрать категорию товара.
    """
    user_id = int(os.getenv('USER_ID'))  # ID пользователя из переменной окружения
    user_name = 'TestUser'

    mock_message = AsyncMock()
    mock_message.from_user.id = user_id
    mock_message.from_user.first_name = user_name
    mock_message.text = 'КАТАЛОГ'

    # Моки для методов message
    mock_message.answer = AsyncMock()

    await catalog(mock_message)

    # Проверяем, что сообщение было отправлено с правильным текстом и клавиатурой
    mock_message.answer.assert_called_once_with(
        'Выберите категорию товара.',
        reply_markup=kb.catalog_list
    )

# Заготовки для дальнейших тестов обработчиков


@pytest.mark.asyncio
async def test_show_category_items_handler():
    """Тестирует обработчик показа элементов категории."""
    pass


@pytest.mark.asyncio
async def test_add_to_cart_handler():
    """Тестирует обработчик добавления товара в корзину."""
    pass


@pytest.mark.asyncio
async def test_show_cart_handler():
    """Тестирует обработчик показа содержимого корзины."""
    pass


@pytest.mark.asyncio
async def test_remove_from_cart_handler():
    """Тестирует обработчик удаления товара из корзины."""
    pass


@pytest.mark.asyncio
async def test_place_order_handler():
    """Тестирует обработчик оформления заказа."""
    pass


@pytest.mark.asyncio
async def test_contacts_handler():
    """Тестирует обработчик показа контактной информации."""
    pass


@pytest.mark.asyncio
async def test_admin_panel():
    """Тестирует обработчик панели администратора."""
    pass


@pytest.mark.asyncio
async def test_add_item_handler():
    """Тестирует обработчик добавления нового товара."""
    pass


@pytest.mark.asyncio
async def test_add_item_type_handler():
    """Тестирует обработчик добавления типа товара."""
    pass


@pytest.mark.asyncio
async def test_cancel_order_handler():
    """Тестирует обработчик отмены заказа."""
    pass


@pytest.mark.asyncio
async def test_add_item_name_handler():
    """Тестирует обработчик добавления названия товара."""
    pass


@pytest.mark.asyncio
async def test_add_item_desc_handler():
    """Тестирует обработчик добавления описания товара."""
    pass


@pytest.mark.asyncio
async def test_add_item_desc_price_handler():
    """Тестирует обработчик добавления описания и цены товара."""
    pass


@pytest.mark.asyncio
async def test_add_item_photo_check_handler():
    """Тестирует обработчик проверки фотографии товара."""
    pass


@pytest.mark.asyncio
async def test_add_item_photo_handler():
    """Тестирует обработчик добавления фото товара."""
    pass


@pytest.mark.asyncio
async def test_show_items_handler():
    """Тестирует обработчик показа всех товаров."""
    pass


@pytest.mark.asyncio
async def test_cancel_operation_handler():
    """Тестирует обработчик отмены операции."""
    pass


@pytest.mark.asyncio
async def test_delete_item_callback_handler():
    """Тестирует обработчик удаления товара по callback."""
    pass


@pytest.mark.asyncio
async def test_answer_handler():
    """Тестирует обработчик ответов на вопросы пользователя."""
    pass
























