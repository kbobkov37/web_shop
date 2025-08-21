import re

class Client:
    """
    Класс клиента
    """
    def __init__(self, name: str, email: str, phone: str, address: str):
        """
        Конструктор класса клиента
        :param name: имя клиента
        :param email: электронная почта
        :param phone: телефон
        :param address: адрес
        """
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

        # Вызов методов валидации для проверки данных при создании объекта
        if not self.is_valid_email():
            raise ValueError(f"Некорректный email: {self.email}")
        if not self.is_valid_phone():
            raise ValueError(f"Некорректный номер телефона: {self.phone}")

    def __str__(self) -> str:
        """
        Строковое представление объекта
        :return:
        """
        return (f"Client("
                f"name='{self.name}', "
                f"email='{self.email}', "
                f"phone='{self.phone}', "
                f"address='{self.address}')")

    def is_valid_email(self) -> bool:
        """
        Проверка валидности email
        :return: True если email валиден, иначе False
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, self.email) is not None

    def is_valid_phone(self) -> bool:
        """
        Проверка валидности номера телефона
        :return: True если номер телефона валиден, иначе False
        """
        pattern = r'^[\+]?[0-9\s\-]{7,15}$'
        return re.match(pattern, self.phone) is not None


class Product:
    """
    Класс товара
    """
    def __init__(self, name: str, price: float, stock: int):
        """
        Конструктор класса товара
        :param name: название товара
        :param price: цена товара
        :param stock: количество на складе
        """
        self.name = name
        self._price = None
        self._stock = None
        self.price = price  # вызовет setter для проверки
        self.stock = stock  # вызовет setter для проверки

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Цена должна быть числом.")
        if value < 0:
            raise ValueError("Цена не может быть отрицательной.")
        self._price = float(value)

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Количество на складе должно быть целым числом.")
        if value < 0:
            raise ValueError("Количество на складе не может быть отрицательным.")
        self._stock = value

    def __str__(self) -> str:
        """
        Строковое представление объекта
        :return:
        """
        return (f"Product("
                f"name='{self.name}', "
                f"price={self.price}, "
                f"stock={self.stock})")


class Order:
    def __init__(self, client_id: int, product_id: int, quantity: int, order_date: str):
        """
        Конструктор класса заказа
        :param client_id: ID клиента
        :param product_id: ID продукта
        :param quantity: количество товара
        :order_date: дата заказа
        """
        if not isinstance(client_id, int):
            raise TypeError("client_id должен быть целым числом.")
        if not isinstance(product_id, int):
            raise TypeError("product_id должен быть целым числом.")
        if not isinstance(quantity, int):
            raise TypeError("quantity должен быть целым числом.")
        if quantity <= 0:
            raise ValueError("quantity должен быть положительным числом.")
        # if not isinstance(order_date, str):
        #     raise TypeError("order_date должен быть целым числом.")

        self.client_id = client_id
        self.product_id = product_id
        self.quantity = quantity
        self.order_date = order_date

    def __str__(self) -> str:
        """
        Строковое представление объекта
        :return:
        """
        return (f"Order("
                f"Client={self.client_id}, "
                f"Product={self.product_id}, "
                f"Quantity={self.quantity}),"
                f"Order_date = {self.order_date}"
                )



