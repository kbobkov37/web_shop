import unittest
from models import Client, Product, Order


class TestClient(unittest.TestCase):
    """
    Набор тестов для класса Client.
    Проверяет корректность создания объекта, валидацию email и телефона,
    а также правильность строкового представления.
    """

    def test_client_creation(self):
        """
        Проверяет корректное создание экземпляра Client с валидными данными.
        Убеждается, что все атрибуты (имя, email, телефон, адрес) установлены верно.
        """
        client = Client("Иван Иванов", "ivan@ivanov.com", "81234567890", "Москва")
        self.assertEqual(client.name, "Иван Иванов")
        self.assertEqual(client.email, "ivan@ivanov.com")
        self.assertEqual(client.phone, "81234567890")
        self.assertEqual(client.address, "Москва")

    def test_valid_email(self):
        """
        Проверяет, что корректный email проходит валидацию.
        Убеждается, что метод is_valid_email() возвращает True для валидного email.
        """
        client = Client("Иван", "ivan@ivanov.com", "81234567890", "Москва")
        self.assertTrue(client.is_valid_email())

    def test_invalid_email_raises_error_on_init(self):
        """
        Проверяет, что при создании клиента с некорректным email выбрасывается ValueError.
        Ожидается исключение при передаче строки, не соответствующей формату email.
        """
        with self.assertRaises(ValueError):
            Client("Иван", "invalid-email", "81234567890", "Москва")

    def test_valid_phone(self):
        """
        Проверяет, что корректный номер телефона проходит валидацию.
        Убеждается, что метод is_valid_phone() возвращает True для номера в формате +7 или 8.
        """
        client = Client("Иван", "ivan@ivanov.com", "81234567890", "Москва")
        self.assertTrue(client.is_valid_phone())

    def test_invalid_phone_raises_error_on_init(self):
        """
        Проверяет, что при создании клиента с некорректным телефоном выбрасывается ValueError.
        Ожидается исключение при передаче строки, не соответствующей формату телефона.
        """
        with self.assertRaises(ValueError):
            Client("Иван", "ivan@ivanov.com", "abc", "Москва")

    def test_str_method(self):
        """
        Проверяет корректность строкового представления объекта Client.
        Убеждается, что метод __str__ возвращает строку в ожидаемом формате.
        """
        client = Client("Иван", "ivan@ivanov.com", "81234567890", "Москва")
        expected = "Client(name='Иван', email='ivan@ivanov.com', phone='81234567890', address='Москва')"
        self.assertEqual(str(client), expected)


class TestProduct(unittest.TestCase):
    """
    Набор тестов для класса Product.
    Проверяет корректность создания объекта, работу сеттеров для price и stock,
    валидацию значений и правильность строкового представления.
    """

    def test_product_creation(self):
        """
        Проверяет корректное создание экземпляра Product с валидными данными.
        Убеждается, что атрибуты name, price и stock установлены верно.
        """
        product = Product("Ноутбук", 50000.0, 10)
        self.assertEqual(product.name, "Ноутбук")
        self.assertEqual(product.price, 50000.0)
        self.assertEqual(product.stock, 10)

    def test_price_setter_valid(self):
        """
        Проверяет, что сеттер цены корректно устанавливает новое значение.
        Убеждается, что price можно изменить на положительное число.
        """
        product = Product("Телефон", 30000, 5)
        product.price = 35000
        self.assertEqual(product.price, 35000.0)

    def test_price_setter_negative(self):
        """
        Проверяет, что попытка установить отрицательную цену вызывает ValueError.
        Ожидается исключение при создании товара с отрицательной ценой.
        """
        with self.assertRaises(ValueError):
            Product("Телефон", -100, 5)

    def test_price_setter_non_numeric(self):
        """
        Проверяет, что попытка установить нечисловую цену вызывает TypeError.
        Ожидается исключение при передаче строки вместо числа.
        """
        with self.assertRaises(TypeError):
            Product("Телефон", "abc", 5)

    def test_stock_setter_valid(self):
        """
        Проверяет, что сеттер количества корректно устанавливает новое значение.
        Убеждается, что stock можно изменить на неотрицательное целое число.
        """
        product = Product("Телефон", 30000, 5)
        product.stock = 8
        self.assertEqual(product.stock, 8)

    def test_stock_setter_negative(self):
        """
        Проверяет, что попытка установить отрицательное количество вызывает ValueError.
        Ожидается исключение при создании товара с отрицательным stock.
        """
        with self.assertRaises(ValueError):
            Product("Телефон", 30000, -1)

    def test_stock_setter_non_integer(self):
        """
        Проверяет, что попытка установить нецелое количество вызывает TypeError.
        Ожидается исключение при передаче float или строки вместо int.
        """
        with self.assertRaises(TypeError):
            Product("Телефон", 30000, 3.5)

    def test_str_method(self):
        """
        Проверяет корректность строкового представления объекта Product.
        Убеждается, что метод __str__ возвращает строку в ожидаемом формате.
        """
        product = Product("Ноутбук", 50000.0, 10)
        expected = "Product(name='Ноутбук', price=50000.0, stock=10)"
        self.assertEqual(str(product), expected)


class TestOrder(unittest.TestCase):
    """
    Набор тестов для класса Order.
    Проверяет корректность создания заказа, валидацию полей (ID, количество),
    типов данных и правильность строкового представления.
    """

    def test_order_creation(self):
        """
        Проверяет корректное создание экземпляра Order с валидными данными.
        Убеждается, что все атрибуты (client_id, product_id, quantity, order_date) установлены верно.
        """
        order = Order(1, 101, 2, '2025-08-22')
        self.assertEqual(order.client_id, 1)
        self.assertEqual(order.product_id, 101)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.order_date, '2025-08-22')

    def test_order_quantity_positive(self):
        """
        Проверяет, что количество товара может быть положительным целым числом.
        Убеждается, что quantity = 1 допустимо.
        """
        order = Order(1, 101, 1, '2025-08-22')
        self.assertEqual(order.quantity, 1)

    def test_order_quantity_zero(self):
        """
        Проверяет, что количество товара не может быть равно нулю.
        Ожидается ValueError при передаче quantity = 0.
        """
        with self.assertRaises(ValueError):
            Order(1, 101, 0, '2025-08-22')

    def test_order_quantity_negative(self):
        """
        Проверяет, что количество товара не может быть отрицательным.
        Ожидается ValueError при передаче отрицательного значения.
        """
        with self.assertRaises(ValueError):
            Order(1, 101, -1, '2025-08-22')

    def test_order_client_id_non_int(self):
        """
        Проверяет, что client_id должен быть целым числом.
        Ожидается TypeError при передаче строки вместо int.
        """
        with self.assertRaises(TypeError):
            Order("1", 101, 2, '2025-08-22')

    def test_order_product_id_non_int(self):
        """
        Проверяет, что product_id должен быть целым числом.
        Ожидается TypeError при передаче строки вместо int.
        """
        with self.assertRaises(TypeError):
            Order(1, "101", 2, '2025-08-22')

    def test_order_quantity_non_int(self):
        """
        Проверяет, что quantity должен быть целым числом.
        Ожидается TypeError при передаче float вместо int.
        """
        with self.assertRaises(TypeError):
            Order(1, 101, 2.5, '2025-08-22')

    def test_str_method(self):
        """
        Проверяет корректность строкового представления объекта Order.
        Убеждается, что метод __str__ возвращает строку в ожидаемом формате.
        """
        order = Order(1, 101, 3, '2025-08-22')
        expected = "Order(Client=1, Product=101, Quantity=3, Order_date='2025-08-22')"
        self.assertEqual(str(order), expected)