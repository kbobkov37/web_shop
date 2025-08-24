import re

class Client:
    """
    Класс, представляющий клиента интернет-магазина.
    Содержит данные о клиенте: имя, email, телефон и адрес.
    При создании объекта автоматически выполняется валидация полей.
    """

    def __init__(self, name: str, email: str, phone: str, address: str):
        """
        Инициализирует объект клиента с валидацией данных.
        Args:
            name (str): Имя клиента. Не может быть пустым.
            email (str): Email клиента. Должен соответствовать стандартному формату.
            phone (str): Номер телефона. Должен начинаться с +7 или 8 и содержать 11 цифр.
            address (str): Адрес клиента. Не может быть пустым.
        Raises:
            ValueError: Если имя, email, телефон или адрес не проходят валидацию.
            TypeError: Не возникает напрямую, но подразумевается при передаче нестроковых значений.
        """
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

        # Валидация при создании
        if not self.name:
            raise ValueError(f"Имя не может быть пустым: {self.name}")
        if not self.is_valid_email():
            raise ValueError(f"Некорректный email: {self.email}")
        if not self.is_valid_phone():
            raise ValueError(f"Некорректный номер телефона: {self.phone}")
        if not self.address:
            raise ValueError(f"Адрес не может быть пустым: {self.address}")

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта Client.
        Returns:
            str: Строка в формате Client(name='...', email='...', phone='...', address='...').
        """
        return (f"Client("
                f"name='{self.name}', "
                f"email='{self.email}', "
                f"phone='{self.phone}', "
                f"address='{self.address}')")

    def is_valid_email(self) -> bool:
        """
        Проверяет, соответствует ли email клиента стандартному формату.
        Используется регулярное выражение для валидации:
        - локальная часть: буквы, цифры, точки, подчёркивания и т.д.
        - домен: должен содержать точку и минимум 2 символа в домене верхнего уровня.
        Returns:
            bool: True, если email валиден, иначе False.
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, self.email) is not None

    def is_valid_phone(self) -> bool:
        """
        Проверяет, соответствует ли номер телефона формату +7XXXXXXXXXX или 8XXXXXXXXXX.
        Номер должен содержать ровно 11 цифр после +7 или 8.
        Returns:
            bool: True, если номер валиден, иначе False.
        """
        pattern = r'^(\+7|8)\d{10}$'
        return re.match(pattern, self.phone) is not None


class Product:
    """
    Класс, представляющий товар в интернет-магазине.
    Содержит название, цену и количество на складе. Валидация данных выполняется через property-сеттеры.
    """

    def __init__(self, name: str, price: float, stock: int):
        """
        Инициализирует объект товара.
        Устанавливает название и использует сеттеры для валидации цены и количества.
        Args:
            name (str): Название товара. Допускается любая строка (проверка на пустоту не обязательна).
            price (float): Цена товара. Должна быть неотрицательным числом.
            stock (int): Количество на складе. Должно быть неотрицательным целым числом.
        Raises:
            TypeError: Если price не число или stock не целое число.
            ValueError: Если price < 0 или stock < 0.
        """
        self.name = name
        self._price = None
        self._stock = None
        self.price = price  # вызовет сеттер
        self.stock = stock  # вызовет сеттер

    @property
    def price(self) -> float:
        """
        Возвращает цену товара.
        Returns:
            float: Текущая цена товара.
        """
        return self._price

    @price.setter
    def price(self, value: float):
        """
        Устанавливает цену товара после валидации.
        Args:
            value (float): Новая цена.
        Raises:
            TypeError: Если значение не является числом (int или float).
            ValueError: Если цена отрицательная.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Цена должна быть числом.")
        if value < 0:
            raise ValueError("Цена не может быть отрицательной.")
        self._price = float(value)

    @property
    def stock(self) -> int:
        """
        Возвращает количество товара на складе.
        Returns:
            int: Текущее количество.
        """
        return self._stock

    @stock.setter
    def stock(self, value: int):
        """
        Устанавливает количество товара на складе после валидации.
        Args:
            value (int): Новое количество.
        Raises:
            TypeError: Если значение не является целым числом.
            ValueError: Если количество отрицательное.
        """
        if not isinstance(value, int):
            raise TypeError("Количество на складе должно быть целым числом.")
        if value < 0:
            raise ValueError("Количество на складе не может быть отрицательным.")
        self._stock = value

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта Product.
        Returns:
            str: Строка в формате Product(name='...', price=..., stock=...).
        """
        return (f"Product("
                f"name='{self.name}', "
                f"price={self.price}, "
                f"stock={self.stock})"
                )


class Order:
    """
    Класс, представляющий заказ в интернет-магазине.
    Связывает клиента и товар по их ID, содержит количество и дату заказа.
    Все входные данные проверяются на корректность при создании.
    """

    def __init__(self, client_id: int, product_id: int, quantity: int, order_date: str):
        """
        Инициализирует объект заказа с валидацией данных.
        Args:
            client_id (int): Уникальный идентификатор клиента.
            product_id (int): Уникальный идентификатор товара.
            quantity (int): Количество товара в заказе. Должно быть положительным.
            order_date (str): Дата заказа в формате строки (например, '2025-04-05').
        Raises:
            TypeError: Если client_id, product_id или quantity не являются целыми числами.
            ValueError: Если quantity не положительное число.
        """
        if not isinstance(client_id, int):
            raise TypeError("client_id должен быть целым числом.")
        if not isinstance(product_id, int):
            raise TypeError("product_id должен быть целым числом.")
        if not isinstance(quantity, int):
            raise TypeError("quantity должен быть целым числом.")
        if quantity <= 0:
            raise ValueError("quantity должен быть положительным числом.")

        self.client_id = client_id
        self.product_id = product_id
        self.quantity = quantity
        self.order_date = order_date

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта Order.
        Returns:
            str: Строка в формате Order(Client=..., Product=..., Quantity=..., Order_date=...).
        """
        return (f"Order("
                f"Client={self.client_id}, "
                f"Product={self.product_id}, "
                f"Quantity={self.quantity}, "
                f"Order_date='{self.order_date}')"
                )