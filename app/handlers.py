import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from main import dp, bot
from app.states import NewOrder
from app.cart import cart
from app import database as db
from app import keyboards as kb
from app.keyboards import (create_keyboard_with_add_to_cart_button,
                           create_remove_from_cart_button,
                           create_place_order_button,
                           create_delete_item_button)


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """
    Обработчик команды /start.

    Args:
        message (types.Message): Объект сообщения от пользователя.

    Returns:
        None
    """
    await db.cmd_start_db(message.from_user.id)  # Выполнение операций при старте бота
    await message.answer_sticker('CAACAgIAAxkBAAMUZbtK1xhqVemnfFwQDUAUAR1wyUUAAo4PAAINxghKa4BZohcI5Jc0BA')
    await message.answer(f'{message.from_user.first_name}, добро пожаловать в спортивный магазин Sport Shop!',
                         reply_markup=kb.main)  # Отправка приветственного сообщения с клавиатурой
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'ВЫ АВТОРИЗОВАЛИСЬ КАК АДМИНИСТРАТОР!', reply_markup=kb.main_admin)


# Обработчик текста "КАТАЛОГ"
@dp.message_handler(text='КАТАЛОГ')
async def catalog(message: types.Message):
    """
    Обработчик текста "КАТАЛОГ".

    Args:
        message (types.Message): Объект сообщения от пользователя.

    Returns:
        None
    """
    await message.answer('Выберите категорию товара.', reply_markup=kb.catalog_list)  # Отображение категорий товаров


# Обработчик нажатия на кнопку категории товара
@dp.callback_query_handler(lambda c: c.data in ['t-shirt', 'sneakers', 'hoodies', 'tracksuits', 'shorts', 'jackets'])
async def show_category_items(callback_query: types.CallbackQuery):
    """
    Обработчик нажатия на кнопку категории товара.

    Args:
        callback_query (types.CallbackQuery): Объект колбэка от пользователя.

    Returns:
        None
    """
    category = callback_query.data
    try:
        items = await db.get_items_by_category(category)  # Получение товаров по выбранной категории
        if items:  # Если есть товары в категории
            for item in items:
                item_id = item[0]
                item_name = item[1]
                item_desc = item[2]
                item_price = item[3]
                item_photo_file_id = item[4]
                item_info = (f"ID: {item_id}\nНАЗВАНИЕ: {item_name}"
                             f"\nОПИСАНИЕ: {item_desc}\nЦЕНА: {item_price}руб.")
                # Отправка информации о товаре и кнопки "Добавить в корзину"
                await bot.send_photo(callback_query.from_user.id, item_photo_file_id)
                keyboard = create_keyboard_with_add_to_cart_button(item_id)
                await bot.send_message(callback_query.from_user.id, item_info, reply_markup=keyboard)
            await bot.send_message(callback_query.from_user.id, 'Для отмены нажмите "Отмена"', reply_markup=kb.cancel)
        else:  # Если в категории нет товаров
            await bot.send_message(callback_query.from_user.id, "В данной категории пока нет товаров")
    except Exception as error:  # Обработка ошибок
        await bot.send_message(callback_query.from_user.id, f"Произошла ошибка: {error}")


# Обработчик нажатия на кнопку "Добавить в корзину"
@dp.callback_query_handler(lambda c: c.data.startswith('add_to_cart_'))
async def add_to_cart(callback_query: types.CallbackQuery):
    """
    Обработчик нажатия на кнопку "Добавить в корзину".

    Args:
        callback_query (types.CallbackQuery): Объект колбэка от пользователя.

    Returns:
        None
    """
    item_id = int(callback_query.data.split('_')[-1])  # Получение ID товара
    item = await db.get_item_by_id(item_id)  # Получение информации о товаре из базы данных
    cart[item_id] = item  # Добавление товара в корзину
    await bot.answer_callback_query(callback_query.id, 'Товар добавлен в корзину')


# Обработчик текста "КОРЗИНА"
@dp.message_handler(text='КОРЗИНА')
async def show_cart(message: types.Message):
    """
    Обработчик текста "КОРЗИНА".

    Args:
        message (types.Message): Объект сообщения от пользователя.

    Returns:
        None
    """
    if cart:  # Если корзина не пуста
        cart_items = []
        cart_info = '\n'.join(cart_items)  # Составление информации о товарах в корзине
        await message.answer(f"ТОВАРЫ В КОРЗИНЕ:\n{cart_info}")  # Отображение информации о товарах
        for item_id, item in cart.items():
            item_id = item[0]
            item_name = item[1]
            item_desc = item[2]
            item_price = item[3]
            item_photo_file_id = item[4]
            await message.answer_photo(item_photo_file_id,  # Отправка фото товара с информацией
                                       caption=f"ID: {item_id}\nНАЗВАНИЕ: "
                                               f"{item_name}\nОПИСАНИЕ: "
                                               f"{item_desc}\nЦЕНА: {item_price}руб.")
        keyboard = types.InlineKeyboardMarkup(row_width=2)  # Создание клавиатуры
        for item_id, item in cart.items():  # Добавление кнопок для удаления товаров из корзины и оформления заказа
            remove_button = create_remove_from_cart_button(item_id, item[1])
            keyboard.add(remove_button)
        place_order_button = create_place_order_button()
        keyboard.add(place_order_button)
        await message.answer("Выберите действие:", reply_markup=keyboard)  # Отображение клавиатуры действий
    else:  # Если корзина пуста
        await message.answer('Корзина пуста')  # Уведомление о пустой корзине


# Обработчик нажатия на кнопку "Удалить из корзины"
@dp.callback_query_handler(lambda c: c.data.startswith('remove_from_cart_'))
async def remove_from_cart(callback_query: types.CallbackQuery):
    """
    Обработчик нажатия на кнопку "Удалить из корзины".

    Args:
        callback_query (types.CallbackQuery): Объект колбэка от пользователя.

    Returns:
        None
    """
    item_id = int(callback_query.data.split('_')[-1])  # Получение ID товара для удаления
    if item_id in cart:  # Если товар найден в корзине
        del cart[item_id]  # Удаление товара из корзины
        await bot.answer_callback_query(callback_query.id, 'Товар удален из корзины')  # Подтверждение удаления
    else:  # Если товар не найден в корзине
        await bot.answer_callback_query(callback_query.id, 'Товар не найден в корзине')  # Уведомление об отсутствии
        # товара в корзине


# Обработчик нажатия на кнопку "Оформить заказ"
@dp.callback_query_handler(text='place_order')
async def place_order(callback_query: types.CallbackQuery):
    """
    Обработчик нажатия на кнопку "Оформить заказ".

    Args:
        callback_query (types.CallbackQuery): Объект колбэка от пользователя.

    Returns:
        None
    """
    await callback_query.answer('Заказ оформлен! Спасибо за ваш заказ!')  # Подтверждение оформления заказа


# Обработчик текста "КОНТАКТЫ"
@dp.message_handler(text='КОНТАКТЫ')
async def contacts(message: types.Message):
    """
    Обработчик текста "КОНТАКТЫ".

    Args:
        message (types.Message): Объект сообщения от пользователя.

    Returns:
        None
    """
    await message.answer('Телеграм продавца: @UltraNumb_coder')  # Отправка контактной информации продавца


# Обработчик текста "Админ-панель"
@dp.message_handler(text='Админ-панель')
async def contacts(message: types.Message):
    """
    Обработчик текста "Админ-панель".

    Args:
        message (types.Message): Объект сообщения от пользователя.

    Returns:
        None
    """
    if message.from_user.id == int(os.getenv('ADMIN_ID')):  # Проверка наличия доступа к админ-панели
        await message.answer('Вы вошли в админ-панель', reply_markup=kb.admin_panel)  # Вход в админ-панель
    else:
        await message.reply('У вас нет доступа к админ-панели!')  # Уведомление об отсутствии доступа


# Обработчик текста "Добавить товар"
@dp.message_handler(text='Добавить товар')
async def add_item(message: types.Message):
    """
    Обработчик текста "Добавить товар".

    Args:
        message (types.Message): Объект сообщения от пользователя.

    Returns:
        None
    """
    if message.from_user.id == int(os.getenv('ADMIN_ID')):  # Проверка наличия доступа к функции добавления товара
        await NewOrder.type.set()  # Установка состояния для оформления нового заказа
        await message.answer('Выберите тип товара', reply_markup=kb.catalog_list)  # Выбор типа товара из списка
    else:
        await message.reply('Я тебя не понимаю!')  # Уведомление об ошибке доступа или непонимании


# Обработчик выбора типа товара
@dp.callback_query_handler(state=NewOrder.type)
async def add_item_type(call: types.CallbackQuery, state: FSMContext):
    """
    Обработчик выбора типа товара.

    Args:
        call (types.CallbackQuery): Объект колбэка от пользователя.
        state (FSMContext): Объект состояния.

    Returns:
        None
    """
    async with state.proxy() as data:
        data['type'] = call.data  # Сохранение выбранного типа товара
    await call.message.answer('Напишите название товара',reply_markup=kb.cancel)  # Запрос на написание
    # названия товара
    await NewOrder.next()  # Переход к следующему шагу в процессе добавления товара


# Обработчик текста "ОТМЕНА" в состоянии добавления товара
@dp.message_handler(text='ОТМЕНА', state=NewOrder)
async def cancel_order(message: types.Message, state: FSMContext):
    """
    Обработчик текста "ОТМЕНА" в состоянии добавления товара.

    Args:
        message (types.Message): Объект сообщения от пользователя.
        state (FSMContext): Объект состояния.

    Returns:
        None
    """
    await state.reset_state()  # Сброс состояния добавления товара
    await message.answer('Операция отменена', reply_markup=kb.main_admin)  # Уведомление об отмене операции
    # с предложением вернуться в главное меню админ-панели


# Обработчик названия товара в состоянии добавления товара
@dp.message_handler(state=NewOrder.name)
async def add_item_name(message: types.Message, state: FSMContext):
    """
    Обработчик названия товара в состоянии добавления товара.

    Args:
        message (types.Message): Объект сообщения от пользователя.
        state (FSMContext): Объект состояния.

    Returns:
        None
    """
    async with state.proxy() as data:
        data['name'] = message.text  # Сохранение введенного названия товара
    await message.answer('Напишите описание товара')  # Запрос на написание описания товара
    await NewOrder.next()  # Переход к следующему шагу в процессе добавления товара


# Обработчик описания товара в состоянии добавления товара
@dp.message_handler(state=NewOrder.desc)
async def add_item_desc(message: types.Message, state: FSMContext):
    """
    Обработчик описания товара в состоянии добавления товара.

    Args:
        message (types.Message): Объект сообщения от пользователя.
        state (FSMContext): Объект состояния.

    Returns:
        None
    """
    async with state.proxy() as data:
        data['desc'] = message.text  # Сохранение введенного описания товара
    await message.answer('Напишите цену товара')  # Запрос на указание цены товара
    await NewOrder.next()  # Переход к следующему шагу в процессе добавления товара


# Обработчик цены товара в состоянии добавления товара
@dp.message_handler(state=NewOrder.price)
async def add_item_desc(message: types.Message, state: FSMContext):
    """
    Обработчик цены товара в состоянии добавления товара.

    Args:
        message (types.Message): Объект сообщения от пользователя.
        state (FSMContext): Объект состояния.

    Returns:
        None
    """
    async with state.proxy() as data:
        data['price'] = message.text  # Сохранение введенной цены товара
    await message.answer('Отправьте фотографию товара')  # Запрос на отправку фотографии товара
    await NewOrder.next()  # Переход к следующему шагу в процессе добавления товара


# Обработчик проверки наличия фотографии в состоянии добавления товара
@dp.message_handler(lambda message: not message.photo, state=NewOrder.photo)
async def add_item_photo_check(message: types.Message):
    """
    Обработчик проверки наличия фотографии в состоянии добавления товара.

    Args:
        message (types.Message): Объект сообщения от пользователя.

    Returns:
        None
    """
    await message.answer('Это не фотография!')  # Уведомление об отправке не фотографии


# Обработчик приема фотографии товара в состоянии добавления товара
@dp.message_handler(content_types=['photo'], state=NewOrder.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    """
    Обработчик приема фотографии товара в состоянии добавления товара.

    Args:
        message (types.Message): Объект сообщения от пользователя.
        state (FSMContext): Объект состояния.

    Returns:
        None
    """
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id  # Сохранение file_id первой фотографии
        item_name = data['name']
        item_price = data['price']
        item_photo_file_id = data['photo']
        await message.answer_photo(item_photo_file_id, caption=f'Товар: {item_name}\nЦена: {item_price}')  # Отображение
        # фотографии товара с информацией о названии и цене

    await db.add_item(state)  # Добавление информации о товаре в базу данных
    await message.answer('Товар успешно создан!', reply_markup=kb.admin_panel)  # Уведомление об успешном создании
    #  товара с предложением вернуться в админ-панель
    await state.finish()  # Сброс состояния добавления товара


# Обработчик текста "Показать товары"
@dp.message_handler(text='Показать товары')
async def show_items(message: types.Message):
    """
    Обработчик текста "Показать товары".

    Args:
        message (types.Message): Объект сообщения от пользователя.

    Returns:
        None
    """
    try:
        items = await db.get_item()  # Получение списка товаров из базы данных

        if items:
            for item in items:
                item_id = item[0]
                item_name = item[1]
                item_desc = item[2]
                item_price = item[3]
                item_photo_file_id = item[4]
                item_info = (f"ID: {item_id}\nНАЗВАНИЕ: {item_name}"
                             f"\nОПИСАНИЕ: {item_desc}"
                             f"\nЦЕНА: {item_price}руб.")
                await message.answer_photo(item_photo_file_id)  # Отображение фотографии товара
                keyboard = create_delete_item_button(item_id)  # Создание кнопки для удаления товара
                await message.answer(item_info, reply_markup=keyboard) # Отображение информации о товаре с кнопкой удаления
            await message.answer('Для отмены нажмите "Отмена"', reply_markup=kb.cancel)  # Предложение отмены операции
        else:
            await message.answer("В базе данных пока нет товаров")  # Уведомление о пустой базе данных
    except Exception as error:
        await message.answer(f"Произошла ошибка: {error}")  # Уведомление об ошибке


# Обработчик текста "ОТМЕНА"
@dp.message_handler(text='ОТМЕНА')
async def cancel_operation(message: types.Message):
    """
    Обработчик текста "ОТМЕНА".

    Args:
        message (types.Message): Объект сообщения от пользователя.

    Returns:
        None
    """
    await message.answer('Операция отменена', reply_markup=kb.main_admin)  # Уведомление об отмене операции
    # с предложением вернуться в главное меню админ-панели


# Обработчик колбэков для удаления товара
@dp.callback_query_handler(lambda c: c.data.startswith('delete_item_'))
async def delete_item_callback(query: types.CallbackQuery):
    """
    Обработчик колбэков для удаления товара.

    Args:
        query (types.CallbackQuery): Объект колбэка от пользователя.

    Returns:
        None
    """
    item_id = int(query.data.split('_')[-1])  # Извлечение ID товара из данных колбэка
    await db.delete_item_by_id(item_id)  # Удаление товара из базы данных по ID
    await query.answer("Товар успешно удален")  # Уведомление об успешном удалении товара


# Обработчик всех остальных сообщений
@dp.message_handler()
async def answer(message: types.Message):
    """
    Обработчик всех остальных сообщений.

    Args:
        message (types.Message): Объект сообщения от пользователя.

    Returns:
        None
    """
    await message.reply('Я тебя не понимаю!') # Ответ на любое сообщение, если нет подходящего обработчика