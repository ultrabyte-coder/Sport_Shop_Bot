# Developer: Aleksandr Kolesnikov

# Документация для телеграм-бота "Sport Shop"

## Введение

Телеграм-бот "Sport Shop" представляет собой онлайн-магазин спортивных товаров, предлагающий пользователям возможность:

- Просматривать каталог товаров
- Добавлять товары в корзину
- Оформлять заказы
- И многое другое

**Этот бот является личной разработкой автора и предоставляется для использования безвозмездно.**
Этот бот является готовым шаблоном, который можно адаптировать под любые магазины. Вы можете изменить его внешний вид и функциональность в соответствии с вашим проектом.

## Структура проекта
.
├── main.py # Основной файл с кодом бота
├── app/
│ ├── init.py # Инициализация модуля
│ ├── database.py # Модуль для работы с базой данных
│ ├── keyboards.py # Модуль для создания клавиатур
│ ├── cart.py # Модуль для хранения товаров в корзине
│ ├── handlers.py # Модуль для функций-обработчиков событий бота
│ └── states.py # Модуль для управления состояниями бота
├── screenshots/ # Скриншоты работы бота
├── tests/ # Тесты бота
├── .env.example # Пример файла конфигурации
├── .gitignore # Список файлов и папок, игнорируемых Git
├── README.md # Документация проекта
└── requirements.txt # Список зависимостей проекта

## Краткое описание модулей

### `main.py`
Содержит основную логику бота, включая обработчики сообщений, настройки и запуск.

### `app/__init__.py`
Инициализирует пакет и обозначает директорию как модуль.

### `app/database.py`
Обеспечивает взаимодействие с базой данных. Позволяет добавлять, удалять и получать товары.

### `app/keyboards.py`
Создает различные типы клавиатур для взаимодействия с пользователями.

### `app/cart.py`
Управляет корзиной пользователя, храня данные о добавленных товарах.

### `app/handlers.py`
Содержит функции-обработчики для различных событий и команд бота.

### `app/states.py`
Определяет состояние бота, позволяя управлять логикой диалога с пользователем.

### `screenshots/`
Включает скриншоты интерфейса бота для наглядности.

### `tests/`
Содержит тесты, проверяющие функциональность бота.

### `.env.example`
Пример того, как прописать важные константы (например, токен бота и ID администратора) для настройки бота.

### `.gitignore`
Файл, указывающий Git, какие файлы и папки не следует отслеживать.

### `README.md`
Документация проекта, содержащая информацию о его структуре и использовании.

### `requirements.txt`
Список всех необходимых библиотек и их версий для корректного запуска проекта.

## Как использовать бота

1. Запустите бота, используя команду `/start`.
2. Используйте команду `КАТАЛОГ`, чтобы просмотреть категории товаров. Выберите интересующий вас товар и добавьте его в корзину.
3. Чтобы просмотреть содержимое корзины, используйте команду `КОРЗИНА`. Вы также можете удалить товары или оформить заказ.
4. Чтобы получить контактные данные продавца, воспользуйтесь командой `КОНТАКТЫ`.
5. В админ-панели доступны следующие функции:
   - `Добавить товары`: добавление новых товаров в базу данных (необходимо указать название, описание, цену и фотографию товара).
   - `Удалить товар`: удаление товара из базы данных (товар не будет отображаться в каталоге после этого).
6. Команда `ОТМЕНА` позволяет отменить последнее действие и вернуться в основное меню.

## Контакты продавца
Если у вас возникли вопросы или предложения, вы можете связаться с продавцом через Телеграм: [@UltraByteCoder](https://t.me/UltraByteCoder).

---

**Важно:** Этот бот предоставляется как есть, без каких-либо гарантий. Любые изменения и усовершенствования остаются на усмотрение пользователя.


# Developer: Aleksandr Kolesnikov

# Documentation for the Telegram Bot "Sport Shop"

## Introduction

The Telegram bot "Sport Shop" serves as an online store for sports goods, offering users the ability to:

- Browse the product catalog
- Add products to the cart
- Place orders
- And much more

**This bot is a personal development by the author and is provided for free use.** 
This bot is a ready-made template that can be adapted for any shops. You can modify its appearance and functionality according to your project.

## Project Structure
.
├── main.py # Main file with the bot's code
├── app/
│ ├── init.py # Module initialization
│ ├── database.py # Module for database interactions
│ ├── keyboards.py # Module for creating keyboards
│ ├── cart.py # Module for storing items in the cart
│ ├── handlers.py # Module for event handler functions of the bot
│ └── states.py # Module for managing bot states
├── screenshots/ # Screenshots of the bot's operation
├── tests/ # Tests for the bot
├── .env.example # Example configuration file
├── .gitignore # List of files and folders ignored by Git
├── README.md # Project documentation
└── requirements.txt # List of project dependencies


## Brief Description of Modules

### `main.py`
Contains the main logic of the bot, including message handlers, settings, and startup.

### `app/__init__.py`
Initializes the package and designates the directory as a module.

### `app/database.py`
Handles interactions with the database. Allows adding, deleting, and retrieving products.

### `app/keyboards.py`
Creates various types of keyboards for user interaction.

### `app/cart.py`
Manages the user's cart, storing data about added products.

### `app/handlers.py`
Contains handler functions for various events and commands of the bot.

### `app/states.py`
Defines the state of the bot, allowing control over the dialog logic with the user.

### `screenshots/`
Includes screenshots of the bot interface for clarity.

### `tests/`
Contains tests that verify the functionality of the bot.

### `.env.example`
An example of how to set important constants (e.g., bot token and admin ID) for configuring the bot.

### `.gitignore`
A file that tells Git which files and folders to ignore.

### `README.md`
Project documentation containing information about its structure and usage.

### `requirements.txt`
A list of all necessary libraries and their versions for the proper functioning of the project.

## How to Use the Bot

1. Start the bot using the command `/start`.
2. Use the command `CATALOG` to view the categories of products. Select the item you are interested in and add it to the cart.
3. To view the contents of the cart, use the command `CART`. You can also remove items or place an order.
4. To get the seller's contact details, use the command `CONTACTS`.
5. The admin panel includes the following functions:
   - `Add Products`: add new products to the database (you need to specify the name, description, price, and photo of the product).
   - `Remove Product`: delete a product from the database (the product will no longer be displayed in the catalog after this).
6. The `CANCEL` command allows you to undo the last action and return to the main menu.

## Seller Contact
If you have any questions or suggestions, you can contact the seller via Telegram: [@UltraByteCoder](https://t.me/UltraByteCoder).

---

**Important:** This bot is provided as-is, without any guarantees. Any changes and improvements are at the user's discretion.
