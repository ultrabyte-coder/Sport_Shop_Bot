import unittest
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.states import NewOrder


class TestNewOrderStates(unittest.TestCase):
    """Тесты для проверки корректности определения и наследования состояний в классе NewOrder."""

    def test_states_definition(self):
        """
        Проверяет, что состояния в классе NewOrder определены корректно.

        В этом тесте мы проверяем, что каждое состояние в классе NewOrder
        является экземпляром класса State. Это гарантирует, что состояния
        правильно настроены для использования в механизме конечных автоматов
        aiogram.

        Состояния, которые мы проверяем:
        - type: Тип заказа
        - name: Имя заказа
        - desc: Описание заказа
        - price: Цена заказа
        - photo: Фото заказа
        """
        self.assertIsInstance(NewOrder.type, State)
        self.assertIsInstance(NewOrder.name, State)
        self.assertIsInstance(NewOrder.desc, State)
        self.assertIsInstance(NewOrder.price, State)
        self.assertIsInstance(NewOrder.photo, State)

    def test_states_names(self):
        """
        Проверяет, что имена состояний в классе NewOrder корректны.

        В этом тесте мы сравниваем ожидаемые имена состояний с фактическими
        именами, которые заданы в классе NewOrder. Корректные имена позволяют
        правильно идентифицировать состояния при работе с конечными автоматами.

        Ожидаемые имена состояний:
        - type: 'NewOrder:type'
        - name: 'NewOrder:name'
        - desc: 'NewOrder:desc'
        - price: 'NewOrder:price'
        - photo: 'NewOrder:photo'
        """
        self.assertEqual(NewOrder.type.state, 'NewOrder:type')
        self.assertEqual(NewOrder.name.state, 'NewOrder:name')
        self.assertEqual(NewOrder.desc.state, 'NewOrder:desc')
        self.assertEqual(NewOrder.price.state, 'NewOrder:price')
        self.assertEqual(NewOrder.photo.state, 'NewOrder:photo')

    def test_states_group_inheritance(self):
        """
        Проверяет, что класс NewOrder наследуется от StatesGroup.

        В этом тесте мы убеждаемся, что класс NewOrder правильно наследует
        функциональность от StatesGroup. Это важно для того, чтобы
        состояния могли быть использованы в контексте диспетчера
        aiogram, обеспечивая правильную работу с состояниями.

        Проверка включает в себя использование функции issubclass для
        подтверждения наследования.
        """
        self.assertTrue(issubclass(NewOrder, StatesGroup))


# Запуск тестов
if __name__ == '__main__':
    unittest.main()

