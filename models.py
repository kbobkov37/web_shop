import re
from db import *

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


# class Statistics____:
#     def __init__(self, db: Database):
#         self.db = db
#
#     def top_5_clients(self):
#         # Получаем все заказы и считаем их по клиентам
#
#         results = self.db.top_5_client()
#         names = [row[1] for row in results]
#         counts = [row[2] for row in results]
#
#         plt.figure(figsize=(8, 6))
#         plt.barh(names, counts)
#         plt.xlabel('Количество заказов')
#         plt.title('Топ-5 клиентов по количеству заказов')
#         plt.gca().invert_yaxis()
#         plt.show()
#
#     def orders_trend(self):
#         # Получаем количество заказов по датам
#         cursor = self.db.conn.cursor()
#         cursor.execute("""
#             SELECT order_date, COUNT(*) FROM Orders
#             GROUP BY order_date
#             ORDER BY order_date
#         """)
#         results = cursor.fetchall()
#         dates = [row[0] for row in results]
#         counts = [row[1] for row in results]
#
#         plt.figure(figsize=(10, 6))
#         plt.plot(dates, counts, marker='o')
#         plt.xlabel('Дата заказа')
#         plt.ylabel('Количество заказов')
#         plt.title('Динамика заказов по датам')
#         plt.xticks(rotation=45)
#         plt.tight_layout()
#         plt.show()
#
#     def clients_products_graph(self):
#         # Строим граф связей клиентов и продуктов (клиенты — вершины, связи — заказы)
#         G = nx.Graph()
#
#         # Получаем все заказы с клиентами и продуктами
#         cursor = self.db.conn.cursor()
#         cursor.execute("""
#             SELECT c.name, p.name FROM Orders o
#             JOIN Clients c ON o.client_id = c.id
#             JOIN Products p ON o.product_id = p.id
#         """)
#         edges = cursor.fetchall()
#
#         # Добавляем узлы клиентов и продуктов
#         clients = set([row[0] for row in edges])
#         products = set([row[1] for row in edges])
#
#         G.add_nodes_from(clients, type='client')
#         G.add_nodes_from(products, type='product')
#
#         # Добавляем связи (ребра)
#         for client_name, product_name in edges:
#             G.add_edge(client_name, product_name)
#
#         # Визуализация графа
#         pos = nx.spring_layout(G)
#
#         client_nodes = [n for n, attr in G.nodes(data=True) if attr['type'] == 'client']
#         product_nodes = [n for n, attr in G.nodes(data=True) if attr['type'] == 'product']
#
#         plt.figure(figsize=(12, 8))
#
#         nx.draw_networkx_nodes(G, pos,
#                                nodelist=client_nodes,
#                                node_color='lightblue',
#                                node_size=500,
#                                label='Клиенты')
#
#         nx.draw_networkx_nodes(G, pos,
#                                nodelist=product_nodes,
#                                node_color='lightgreen',
#                                node_size=500,
#                                label='Продукты')
#
#         nx.draw_networkx_edges(G, pos)
#
#         nx.draw_networkx_labels(G, pos)
#
#         plt.title('Граф связей клиентов и продуктов')
#
#         # Создаем легенду вручную
#         import matplotlib.patches as mpatches
#
#     legend_handles = [
#         mpatches.Patch(color='lightblue', label='Клиенты'),
#         mpatches.Patch(color='lightgreen', label='Продукты')
#     ]
#     plt.legend(handles=legend_handles)
#
#     plt.axis('off')
#     plt.show()


# class Statistics:
#     def __init__(self, parent, db: Database):
#         self.parent = parent
#         self.db = db
#
#         # Создаем LabelFrame для каждого вида статистики
#         self.top_clients_frame = ttk.LabelFrame(parent, text="Топ-5 клиентов")
#         self.top_clients_frame.pack(fill='both', expand=True, padx=10, pady=10)
#
#         self.orders_trend_frame = ttk.LabelFrame(parent, text="Динамика заказов")
#         self.orders_trend_frame.pack(fill='both', expand=True, padx=10, pady=10)
#
#         self.clients_products_frame = ttk.LabelFrame(parent, text="Граф связей клиентов и продуктов")
#         self.clients_products_frame.pack(fill='both', expand=True, padx=10, pady=10)
#
#         # Вызов методов для отображения графиков внутри LabelFrame
#         self.show_top_5_clients()
#         self.show_orders_trend()
#         self.show_clients_products_graph()
#
#     def show_top_5_clients(self):
#         cursor = self.db.conn.cursor()
#         cursor.execute("""
#             SELECT c.id, c.name, COUNT(o.id) as order_count
#             FROM Clients c
#             LEFT JOIN Orders o ON c.id = o.client_id
#             GROUP BY c.id, c.name
#             ORDER BY order_count DESC
#             LIMIT 5
#         """)
#         results = cursor.fetchall()
#         names = [row[1] for row in results]
#         counts = [row[2] for row in results]
#
#         fig, ax = plt.subplots(figsize=(6, 4))
#         ax.barh(names, counts)
#         ax.set_xlabel('Количество заказов')
#         ax.set_title('Топ-5 клиентов по заказам')
#         ax.invert_yaxis()
#
#         canvas = FigureCanvasTkAgg(fig, master=self.top_clients_frame)
#         canvas.draw()
#         canvas.get_tk_widget().pack(fill='both', expand=True)
#
#     def show_orders_trend(self):
#         cursor = self.db.conn.cursor()
#         cursor.execute("""
#             SELECT order_date, COUNT(*) FROM Orders
#             GROUP BY order_date
#             ORDER BY order_date
#         """)
#         results = cursor.fetchall()
#         dates = [row[0] for row in results]
#         counts = [row[1] for row in results]
#
#         fig, ax = plt.subplots(figsize=(6, 4))
#         ax.plot(dates, counts, marker='o')
#         ax.set_xlabel('Дата заказа')
#         ax.set_ylabel('Количество заказов')
#         ax.set_title('Динамика заказов по датам')
#         plt.setp(ax.get_xticklabels(), rotation=45)
#
#         canvas = FigureCanvasTkAgg(fig, master=self.orders_trend_frame)
#         canvas.draw()
#         canvas.get_tk_widget().pack(fill='both', expand=True)
#
#     def show_clients_products_graph(self):
#         G = nx.Graph()
#
#         cursor = self.db.conn.cursor()
#         cursor.execute("""
#             SELECT c.name, p.name FROM Orders o
#             JOIN Clients c ON o.client_id = c.id
#             JOIN Products p ON o.product_id = p.id
#         """)
#         edges = cursor.fetchall()
#
#         clients = set([row[0] for row in edges])
#         products = set([row[1] for row in edges])
#
#         G.add_nodes_from(clients, type='client')
#         G.add_nodes_from(products, type='product')
#
#         for client_name, product_name in edges:
#             G.add_edge(client_name, product_name)
#
#         pos = nx.spring_layout(G)
#
#         fig, ax = plt.subplots(figsize=(8, 6))
#
#         client_nodes = [n for n, attr in G.nodes(data=True) if attr['type'] == 'client']
#         product_nodes = [n for n, attr in G.nodes(data=True) if attr['type'] == 'product']
#
#         nx.draw_networkx_nodes(G, pos,
#                                nodelist=client_nodes,
#                                node_color='lightblue',
#                                node_size=500,
#                                label='Клиенты',
#                                ax=ax)
#
#         nx.draw_networkx_nodes(G, pos,
#                                nodelist=product_nodes,
#                                node_color='lightgreen',
#                                node_size=500,
#                                label='Продукты',
#                                ax=ax)
#
#         nx.draw_networkx_edges(G, pos, ax=ax)
#
#         # Лейблы и легенда
#
#     nx.draw_networkx_labels(G, pos, ax=ax)
#     legend_handles = [
#         plt.Line2D([0], [0], marker='o', color='w', label='Клиенты',
#                    markerfacecolor='lightblue', markersize=10),
#         plt.Line2D([0], [0], marker='o', color='w', label='Продукты',
#                    markerfacecolor='lightgreen', markersize=10)
#     ]
#     ax.legend(handles=legend_handles)
#     ax.set_title('Граф связей клиентов и продуктов')
#     ax.axis('off')
#
#     canvas = FigureCanvasTkAgg(fig, master=self.clients_products_frame)
#     canvas.draw()
#     canvas.get_tk_widget().pack(fill='both', expand=True)