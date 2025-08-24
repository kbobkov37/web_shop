import sqlite3
import pandas as pd

DB_NAME = "store.db"


class Database:
    """
    Класс для работы с SQLite-базой данных интернет-магазина.
    Предоставляет методы для создания таблиц, управления клиентами, товарами и заказами,
    а также для получения статистики и отчётов. Использует контекстные менеджеры для
    автоматического управления транзакциями.
    """

    def __init__(self, db_name=DB_NAME):
        """
        Инициализирует подключение к базе данных и создаёт таблицы при необходимости.
        Args:
            db_name (str): Путь к файлу базы данных. По умолчанию — 'store.db'.
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """
        Создаёт таблицы Clients, Products и Orders, если они ещё не существуют.
        Таблицы:
            - Clients: хранит данные клиентов.
            - Products: хранит данные о товарах (с проверкой на неотрицательные цена и остаток).
            - Orders: хранит заказы с внешними ключами на клиентов и товары.
        """
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS Clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    c_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    address TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS Products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    p_name TEXT NOT NULL,
                    price REAL NOT NULL CHECK (price >= 0),
                    stock INTEGER NOT NULL CHECK (stock >= 0)
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS Orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id INTEGER,
                    product_id INTEGER,
                    quantity INTEGER NOT NULL,
                    order_date TEXT NOT NULL,
                    FOREIGN KEY (client_id) REFERENCES Clients (id),
                    FOREIGN KEY (product_id) REFERENCES Products (id)
                )
            """)
            self.conn.commit()

    # ----- Работа с клиентами -----

    def insert_client(self, c_name: str, email: str, phone: str, address: str) -> None:
        """
        Добавляет нового клиента в таблицу Clients.
        Args:
            c_name (str): Полное имя клиента.
            email (str): Электронная почта клиента.
            phone (str): Номер телефона клиента.
            address (str): Адрес клиента.
        """
        with self.conn:
            self.cursor.execute(
                "INSERT INTO Clients (c_name, email, phone, address) VALUES (?, ?, ?, ?)",
                (c_name, email, phone, address)
            )
            self.conn.commit()

    def load_client(self) -> list[tuple]:
        """
        Загружает всех клиентов из таблицы Clients.
        Returns:
            list[tuple]: Список кортежей с данными клиентов: (id, c_name, email, phone, address).
        """
        with self.conn:
            self.cursor.execute("SELECT * FROM Clients")
            return self.cursor.fetchall()

    def get_clients(self) -> list[tuple]:
        """
        Получает список всех клиентов с их ID и именами.
        Используется, например, для заполнения выпадающих списков.
        Returns:
            list[tuple]: Список кортежей (id, c_name).
        """
        with self.conn:
            self.cursor.execute("SELECT id, c_name FROM Clients")
            return self.cursor.fetchall()

    def get_client_id(self, cl_name: str) -> tuple | None:
        """
        Находит ID клиента по его имени.
        Args:
            cl_name (str): Имя клиента.
        Returns:
            tuple | None: Кортеж с ID клиента или None, если клиент не найден.
        """
        with self.conn:
            self.cursor.execute("SELECT id FROM Clients WHERE c_name = ?", (cl_name,))
            return self.cursor.fetchone()

    def update_client(self, client_id: int, c_name: str = None, email: str = None,
                      phone: str = None, address: str = None) -> None:
        """
        Обновляет данные клиента частично (только указанные поля).
        Args:
            client_id (int): ID клиента для обновления.
            c_name (str, optional): Новое имя.
            email (str, optional): Новый email.
            phone (str, optional): Новый телефон.
            address (str, optional): Новый адрес.
        """
        fields = []
        params = []

        if c_name is not None:
            fields.append("c_name = ?")
            params.append(c_name)
        if email is not None:
            fields.append("email = ?")
            params.append(email)
        if phone is not None:
            fields.append("phone = ?")
            params.append(phone)
        if address is not None:
            fields.append("address = ?")
            params.append(address)

        if not fields:
            return  # Нечего обновлять

        params.append(client_id)

        with self.conn:
            self.cursor.execute(
                f"UPDATE Clients SET {', '.join(fields)} WHERE id = ?",
                params
            )
            self.conn.commit()

    def delete_client(self, client_id: int) -> None:
        """
        Удаляет клиента из базы данных по ID.
        Args:
            client_id (int): ID клиента для удаления.
        """
        with self.conn:
            self.cursor.execute("DELETE FROM Clients WHERE id = ?", (client_id,))
            self.conn.commit()

    # ----- Работа с товарами -----

    def insert_product(self, p_name: str, price: float, stock: int) -> None:
        """
        Добавляет новый товар в таблицу Products.
        Args:
            p_name (str): Название товара.
            price (float): Цена товара (должна быть >= 0).
            stock (int): Количество на складе (должно быть >= 0).
        """
        with self.conn:
            self.cursor.execute(
                "INSERT INTO Products (p_name, price, stock) VALUES (?, ?, ?)",
                (p_name, price, stock)
            )
            self.conn.commit()

    def load_product(self) -> list[tuple]:
        """
        Загружает все товары из таблицы Products.
        Returns:
            list[tuple]: Список кортежей с данными товаров: (id, p_name, price, stock).
        """
        with self.conn:
            self.cursor.execute("SELECT * FROM Products")
            return self.cursor.fetchall()

    def get_products(self) -> list[tuple]:
        """
        Получает список всех товаров с их ID и наименованиями.
        Используется для заполнения выпадающих списков.
        Returns:
            list[tuple]: Список кортежей (id, p_name).
        """
        with self.conn:
            self.cursor.execute("SELECT id, p_name FROM Products")
            return self.cursor.fetchall()

    def get_product_id(self, pr_name: str) -> tuple | None:
        """
        Находит ID товара по его наименованию.
        Args:
            pr_name (str): Название товара.
        Returns:
            tuple | None: Кортеж с ID товара или None, если товар не найден.
        """
        with self.conn:
            self.cursor.execute("SELECT id FROM Products WHERE p_name = ?", (pr_name,))
            return self.cursor.fetchone()

    def update_product(self, product_id: int, p_name: str = None, price: float = None,
                       stock: int = None) -> None:
        """
        Обновляет данные товара частично (только указанные поля).
        Args:
            product_id (int): ID товара для обновления.
            p_name (str, optional): Новое название.
            price (float, optional): Новая цена.
            stock (int, optional): Новое количество на складе.
        """
        fields = []
        params = []

        if p_name is not None:
            fields.append("p_name = ?")
            params.append(p_name)
        if price is not None:
            fields.append("price = ?")
            params.append(price)
        if stock is not None:
            fields.append("stock = ?")
            params.append(stock)

        if not fields:
            return

        params.append(product_id)

        with self.conn:
            self.cursor.execute(
                f"UPDATE Products SET {', '.join(fields)} WHERE id = ?",
                params
            )
            self.conn.commit()

    def delete_product(self, product_id: int) -> None:
        """
        Удаляет товар из базы данных по ID.
        Args:
            product_id (int): ID товара для удаления.
        """
        with self.conn:
            self.cursor.execute("DELETE FROM Products WHERE id = ?", (product_id,))
            self.conn.commit()

    # ----- Работа с заказами -----

    def insert_order(self, client_id: int, product_id: int, quantity: int, order_date: str) -> None:
        """
        Добавляет новый заказ в таблицу Orders.
        Args:
            client_id (int): ID клиента.
            product_id (int): ID товара.
            quantity (int): Количество товара в заказе.
            order_date (str): Дата заказа в формате 'YYYY-MM-DD'.
        """
        with self.conn:
            self.conn.execute(
                "INSERT INTO Orders (client_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)",
                (client_id, product_id, quantity, order_date)
            )
            self.conn.commit()

    def load_order(self) -> list[tuple]:
        """
        Загружает все заказы с именами клиентов и товаров.
        Выполняет JOIN с таблицами Clients и Products для отображения человекочитаемых данных.
        Returns:
            list[tuple]: Список кортежей: (order_id, client_name, product_name, quantity, order_date).
        """
        with self.conn:
            self.cursor.execute("""
                SELECT 
                    o.id AS order_id,
                    c.c_name AS "Клиент",
                    p.p_name AS "Товар",
                    o.quantity AS "Количество",
                    o.order_date AS "Дата заказа"
                FROM Orders o
                JOIN Clients c ON o.client_id = c.id
                JOIN Products p ON o.product_id = p.id
            """)
            return self.cursor.fetchall()

    def update_order(self, order_id: int, client_id: int = None, product_id: int = None,
                     quantity: int = None, order_date: str = None) -> None:
        """
        Обновляет данные заказа частично (только указанные поля).
        Args:
            order_id (int): ID заказа для обновления.
            client_id (int, optional): Новый ID клиента.
            product_id (int, optional): Новый ID товара.
            quantity (int, optional): Новое количество.
            order_date (str, optional): Новая дата заказа.
        """
        fields = []
        params = []

        if client_id is not None:
            fields.append("client_id = ?")
            params.append(client_id)
        if product_id is not None:
            fields.append("product_id = ?")
            params.append(product_id)
        if quantity is not None:
            fields.append("quantity = ?")
            params.append(quantity)
        if order_date is not None:
            fields.append("order_date = ?")
            params.append(order_date)

        if not fields:
            return

        params.append(order_id)

        with self.conn:
            self.cursor.execute(
                f"UPDATE Orders SET {', '.join(fields)} WHERE id = ?",
                params
            )
            self.conn.commit()

    def delete_order(self, order_id: int) -> None:
        """
        Удаляет заказ из базы данных по ID.
        Args:
            order_id (int): ID заказа для удаления.
        """
        with self.conn:
            self.cursor.execute("DELETE FROM Orders WHERE id = ?", (order_id,))
            self.conn.commit()

    # ----- Работа с отчетами и статистикой -----

    def get_datas(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Загружает данные из всех таблиц в виде pandas DataFrame.
        Используется для анализа и построения графиков.
        Returns:
            tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Кортеж из трёх DataFrame:
                - orders_df: заказы,
                - clients_df: клиенты,
                - products_df: товары.
        """
        with self.conn:
            orders_df = pd.read_sql_query("SELECT * FROM Orders", self.conn)
            clients_df = pd.read_sql_query("SELECT * FROM Clients", self.conn)
            products_df = pd.read_sql_query("SELECT * FROM Products", self.conn)
            return orders_df, clients_df, products_df

    def top_5_client(self) -> list[tuple]:
        """
        Получает топ-5 клиентов по количеству заказов.
        Returns:
            list[tuple]: Список кортежей: (client_id, client_name, order_count).
        """
        with self.conn:
            self.cursor.execute("""
                SELECT c.id, c.c_name, COUNT(o.id) as order_count
                FROM Clients c
                LEFT JOIN Orders o ON c.id = o.client_id
                GROUP BY c.id, c.c_name
                ORDER BY order_count DESC
                LIMIT 5
            """)
            return self.cursor.fetchall()

    def show_order_trend(self) -> list[tuple]:
        """
        Получает количество заказов по датам для анализа динамики.
        Returns:
            list[tuple]: Список кортежей: (order_date, count).
        """
        with self.conn:
            self.cursor.execute("""
                SELECT order_date, COUNT(*) 
                FROM Orders
                GROUP BY order_date
                ORDER BY order_date
            """)
            return self.cursor.fetchall()

    def show_client_product_graph(self) -> list[tuple]:
        """
        Получает связи клиентов и купленных товаров для построения графа.
        Returns:
            list[tuple]: Список кортежей: (client_name, product_name).
        """
        with self.conn:
            self.cursor.execute("""
                SELECT c.c_name, p.p_name 
                FROM Orders o
                JOIN Clients c ON o.client_id = c.id
                JOIN Products p ON o.product_id = p.id
            """)
            return self.cursor.fetchall()