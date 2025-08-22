import sqlite3
import pandas as pd

DB_NAME = "store.db"

class Database:
    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
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

# ----- Работа с клиентами
    def insert_client(self, c_name, email, phone, address):
        """
        Добавление нового клиента в БД
        :param c_name:
        :param email:
        :param phone:
        :param address:
        :return:
        """
        with self.conn:
            self.cursor.execute(
                "INSERT INTO Clients (c_name, email, phone, address) VALUES (?, ?, ?, ?)",
                (c_name, email, phone, address)
            )
            self.conn.commit()

    def load_client(self):
        """
        Выборка всех клиентов из БД
        :return: 
        """
        with self.conn:
            self.cursor.execute("SELECT * FROM Clients")
            return self.cursor.fetchall()

    def get_clients(self):
        """
        Выборка ИД и имен клиентов из таблицы клиентов
        :return:
        """
        with self.conn:
            self.cursor.execute("SELECT id, c_name FROM Clients")

            return self.cursor.fetchall()

    def update_client(self, client_id, c_name=None, email=None, phone=None, address=None):
        """
        Обновляет список клиентов, для отображения в таблице
        :param client_id:
        :param c_name:
        :param email:
        :param phone:
        :param address:
        :return:
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
            self.conn.execute(
                f"UPDATE Clients SET {', '.join(fields)} WHERE id = ?",
                params
            )
            self.conn.commit()

    def delete_client(self, client_id):
        """
        Удаляет выбранного клиента из БД
        :param client_id:
        :return:
        """
        with self.conn:
            self.cursor.execute("DELETE FROM Clients WHERE id = ?", (client_id,))
            self.conn.commit()

# ----- Работа с товарами
    def insert_product(self, p_name, price, stock):
        """
        Добавляет товар в БД
        :param p_name:
        :param price:
        :param stock:
        :return:
        """
        with self.conn:
            self.cursor.execute(
                "INSERT INTO Products (p_name, price, stock) VALUES (?, ?, ?)",
                (p_name, price, stock)
            )
            self.conn.commit()

    def load_product(self):
        """
        Выборка всех товаров из БД
        :return:
        """
        with self.conn:
            self.cursor.execute("SELECT * FROM Products")

            return self.cursor.fetchall()

    def get_products(self):
        """
        Выборка ИД и наименования товара из таблицы товаров
        :return:
        """
        with self.conn:
            self.cursor.execute("SELECT id, p_name FROM Products")

            return self.cursor.fetchall()

    def update_product(self, product_id, p_name=None, price=None, stock=None):
        """
        Обновляет список товаров, для отображения в таблице
        :param product_id:
        :param p_name:
        :param price:
        :param stock:
        :return:
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

    def delete_product(self, product_id):
        """
        Удаляет продукт из БД
        :param product_id:
        :return:
        """
        with self.conn:
            self.cursor.execute("DELETE FROM Products WHERE id = ?", (product_id,))
            self.conn.commit()

# ----- Работа с заказами
    def insert_order(self, client_id, product_id, quantity, order_date):
        """
        Добавляет заказ в БД
        :param client_id:
        :param product_id:
        :param quantity:
        :param order_date:
        :return:
        """
        with self.conn:
            self.conn.execute(
                "INSERT INTO Orders (client_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)",
                (client_id, product_id, quantity, order_date)
            )
            self.conn.commit()

    # def load_order(self):
    #     """
    #     Выборка всех заказов из БД
    #     :return:
    #     """
    #     with self.conn:
    #         self.cursor.execute("SELECT * FROM Orders")
    #
    #         return self.cursor.fetchall()

    def load_order(self):
        """
        Выборка всех заказов из БД
        :return:
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

    # def get_orders(self):
    #     """
    #     Выборка для заполнения таблицы заказов
    #     :return:
    #     """
    #     with self.conn:
    #         query = """
    #                   SELECT o.id, c.c_name, p.p_name, o.quantity, o.order_date
    #                   FROM Orders o
    #                   JOIN Clients c ON o.client_id = c.id
    #                   JOIN Products p ON o.product_id = p.id
    #                       """
    #         self.cursor.execute(query)
    #
    #         return self.cursor.fetchall()

    def update_order(self, order_id, client_id=None, product_id=None, quantity=None, order_date=None):
        """
        Обновление таблицы с заказами
        :param order_id:
        :param client_id:
        :param product_id:
        :param quantity:
        :param order_date:
        :return:
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
            self.conn.execute(
                f"UPDATE Orders SET {', '.join(fields)} WHERE id = ?",
                params
            )
            self.conn.commit()

    def delete_order(self, order_id):
        """
        Удаление заказа
        :param order_id:
        :return:
        """
        with self.conn:
            self.cursor.execute("DELETE FROM Orders WHERE id = ?", (order_id,))
            self.conn.commit()

# ----- Работа с отчетами и статистикой

    def get_data(self):
        """
        Сбор данных в датафреймы
        :return:
        """
        with self.conn:
            orders_df = pd.read_sql_query("SELECT * FROM Orders", self.conn)
            clients_df = pd.read_sql_query("SELECT * FROM Clients", self.conn)
            products_df = pd.read_sql_query("SELECT * FROM Products", self.conn)

            return orders_df, clients_df, products_df

