from aiogram.dispatcher.filters.state import State, StatesGroup


# Определение состояний для оформления нового заказа
class NewOrder(StatesGroup):
    """
    Класс для определения состояний при оформлении нового заказа.

    Attributes:
        type (State): Состояние для выбора типа товара.
        name (State): Состояние для ввода названия товара.
        desc (State): Состояние для ввода описания товара.
        price (State): Состояние для ввода цены товара.
        photo (State): Состояние для отправки фотографии товара.
    """
    type = State()
    name = State()
    desc = State()
    price = State()
    photo = State()

