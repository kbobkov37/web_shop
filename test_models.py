import unittest
from models import Client, Product, Order


class TestClient(unittest.TestCase):
    def test_client_creation(self):
        client = Client("Иван Иванов", "ivan@example.com", "+7 900 123-45-67", "Москва")
        self.assertEqual(client.name, "Иван Иванов")
        self.assertEqual(client.email, "ivan@example.com")
        self.assertEqual(client.phone, "+7 900 123-45-67")
        self.assertEqual(client.address, "Москва")

    def test_valid_email(self):
        client = Client("Иван", "ivan@example.com", "1234567", "Москва")
        self.assertTrue(client.is_valid_email())

    def test_invalid_email(self):
        client = Client("Иван", "invalid-email", "1234567", "Москва")
        self.assertFalse(client.is_valid_email())

    def test_invalid_email_raises_error_on_init(self):
        with self.assertRaises(ValueError):
            Client("Иван", "invalid-email", "1234567", "Москва")

    def test_valid_phone(self):
        client = Client("Иван", "ivan@example.com", "+7 900 123-45-67", "Москва")
        self.assertTrue(client.is_valid_phone())

    def test_invalid_phone(self):
        client = Client("Иван", "ivan@example.com", "abc", "Москва")
        self.assertFalse(client.is_valid_phone())

    def test_invalid_phone_raises_error_on_init(self):
        with self.assertRaises(ValueError):
            Client("Иван", "ivan@example.com", "abc", "Москва")

    def test_str_method(self):
        client = Client("Иван", "ivan@example.com", "1234567", "Москва")
        expected = "Client(name='Иван', email='ivan@example.com', phone='1234567', address='Москва')"
        self.assertEqual(str(client), expected)


class TestProduct(unittest.TestCase):
    def test_product_creation(self):
        product = Product("Ноутбук", 50000.0, 10)
        self.assertEqual(product.name, "Ноутбук")
        self.assertEqual(product.price, 50000.0)
        self.assertEqual(product.stock, 10)

    def test_price_setter_valid(self):
        product = Product("Телефон", 30000, 5)
        product.price = 35000
        self.assertEqual(product.price, 35000.0)

    def test_price_setter_negative(self):
        with self.assertRaises(ValueError):
            Product("Телефон", -100, 5)

    def test_price_setter_non_numeric(self):
        with self.assertRaises(TypeError):
            Product("Телефон", "abc", 5)

    def test_stock_setter_valid(self):
        product = Product("Телефон", 30000, 5)
        product.stock = 8
        self.assertEqual(product.stock, 8)

    def test_stock_setter_negative(self):
        with self.assertRaises(ValueError):
            Product("Телефон", 30000, -1)

    def test_stock_setter_non_integer(self):
        with self.assertRaises(TypeError):
            Product("Телефон", 30000, 3.5)

    def test_str_method(self):
        product = Product("Ноутбук", 50000.0, 10)
        expected = "Product(name='Ноутбук', price=50000.0, stock=10)"
        self.assertEqual(str(product), expected)


class TestOrder(unittest.TestCase):
    def test_order_creation(self):
        order = Order(1, 101, 2)
        self.assertEqual(order.client_id, 1)
        self.assertEqual(order.product_id, 101)
        self.assertEqual(order.quantity, 2)

    def test_order_quantity_positive(self):
        order = Order(1, 101, 1)
        self.assertEqual(order.quantity, 1)

    def test_order_quantity_zero(self):
        with self.assertRaises(ValueError):
            Order(1, 101, 0)

    def test_order_quantity_negative(self):
        with self.assertRaises(ValueError):
            Order(1, 101, -1)

    def test_order_client_id_non_int(self):
        with self.assertRaises(TypeError):
            Order("1", 101, 2)

    def test_order_product_id_non_int(self):
        with self.assertRaises(TypeError):
            Order(1, "101", 2)

    def test_order_quantity_non_int(self):
        with self.assertRaises(TypeError):
            Order(1, 101, 2.5)

    def test_str_method(self):
        order = Order(1, 101, 3)
        expected = "Order(Client=1, Product=101, Quantity=3)"
        self.assertEqual(str(order), expected)


# if __name__ == '__main__':
#     unittest.main()