# import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Label, Entry, Button, Frame, filedialog, StringVar
# import sqlite3
# import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from datetime import datetime
import os
import csv
from tkinter import *
from app import *
from db import *
from models import *

class MainApp:
    """
    Главное окно приложения. в нем расположено 5 кнопок: Клиенты, Товары, Заказы,
    Статистика, Выход. При нажатии на любую кнопку открывается дополнительное окно,
    с соответствующим функционалом.
    """
    def __init__(self, root):
        """
        Конструктор класса
        :param root:
        """
        self.root = root
        self.root.title("Управление интернет-магазином")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        title = tk.Label(self.root,
                         text="Управление интернет-магазина",
                         font=("Arial", 18),
                         pady=20)
        title.pack()

        buttons = [
            ("Клиенты", self.open_clients_window),
            ("Товары", self.open_products_window),
            ("Заказы", self.open_orders_window),
            ("Статистика", self.open_stats_window),
            ("Выход", self.exit_app)
        ]

        for text, command in buttons:
            btn = tk.Button(self.root,
                            text=text,
                            font=("Arial", 14),
                            width=20,
                            height=1, command=command)
            btn.pack(pady=5)

    def open_clients_window(self):
        """
        Метод открытия окна для добавления, удаления, редактирования, поиска клиентов
        """
        ClientsWindow(Toplevel(self.root))

    def open_products_window(self):
        """
        Метод открытия окна для добавления, удаления, редактирования, поиска товаров
        """
        ProductsWindow(Toplevel(self.root))

    def open_orders_window(self):
        """
        Метод открытия окна для добавления, удаления, редактирования, поиска заказов
        """
        OrdersWindow(Toplevel(self.root))

    def open_stats_window(self):
        """
        Метод открытия окна с различной статистикой
        """
        StatsWindow(Toplevel(self.root))

    def exit_app(self):
        """
        Выход из приложения с подтверждением
        """
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.root.quit()

class StatsWindow:
    """
    Окно статистики
    """
    def __init__(self, window):
        self.window = window
        self.window.title("Статистика")
        self.window.geometry("800x600")

        frame = Frame(self.window, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        Button(frame, text="Показать топ-5 клиентов", command=self.top_clients).pack(pady=5)
        Button(frame, text="Динамика заказов", command=self.order_trend).pack(pady=5)
        Button(frame, text="Граф связей клиентов", command=self.client_network).pack(pady=5)
        Button(frame, text="Выйти", command=self.window.destroy).pack(pady=10)

    def get_data(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            orders_df = pd.read_sql_query("SELECT * FROM Orders", conn)
            clients_df = pd.read_sql_query("SELECT * FROM Clients", conn)
            products_df = pd.read_sql_query("SELECT * FROM Products", conn)
            conn.close()
            return orders_df, clients_df, products_df
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки данных: {e}")
            return None, None, None

    def top_clients(self):
        orders_df, clients_df, _ = self.get_data()
        if orders_df is None:
            return

        top = orders_df.groupby('client_id').size().nlargest(5).reset_index(name='count')
        top = top.merge(clients_df[['id', 'name']], left_on='client_id', right_on='id')
        top = top[['name', 'count']]

        plt.figure(figsize=(8, 5))
        sns.barplot(data=top, x='count', y='name', palette='viridis')
        plt.title("Топ-5 клиентов по количеству заказов")
        plt.xlabel("Количество заказов")
        plt.ylabel("Клиент")
        plt.tight_layout()
        plt.show()

    def order_trend(self):
        orders_df, _, _ = self.get_data()
        if orders_df is None:
            return

        orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
        trend = orders_df.groupby('order_date').size()

        plt.figure(figsize=(10, 5))
        sns.lineplot(data=trend, marker='o')
        plt.title("Динамика заказов по датам")
        plt.xlabel("Дата")
        plt.ylabel("Количество заказов")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def client_network(self):
        orders_df, clients_df, _ = self.get_data()
        if orders_df is None:
            return

        # Граф по общим товарам
        G = nx.Graph()
        client_products = orders_df.groupby('client_id')['product_id'].apply(set)

        clients = list(client_products.index)
        for i in range(len(clients)):
            for j in range(i + 1, len(clients)):
                common = client_products[clients[i]] & client_products[clients[j]]
                if len(common) > 0:
                    name1 = clients_df[clients_df['id'] == clients[i]]['name'].values[0]
                    name2 = clients_df[clients_df['id'] == clients[j]]['name'].values[0]
                    G.add_edge(name1, name2, weight=len(common))

        if G.number_of_edges() == 0:
            messagebox.showinfo("Граф", "Нет связанных клиентов по товарам.")
            return

        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G, k=0.5)
        nx.draw(G, pos, with_labels=True, node_size=800, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.title("Граф связей клиентов (по общим товарам)")
        plt.tight_layout()
        plt.show()

class ClientsWindow:
    """
    Окно управления клиентами
    """
    def __init__(self, window):
        """
        Конструктор класса создания новых клиентов
        :param window:
        """
        self.window = window
        self.window.title("Клиенты")
        self.window.geometry("1000x700")
        self.db = Database()

        frame = Frame(self.window, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        # --- Поиск ---
        search_frame = Frame(frame)
        search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        Label(search_frame, text="Поиск:").pack(side="left", padx=5)
        self.search_var = StringVar()
        self.search_var.trace("w", self.filter_clients)  # Live search
        Entry(search_frame, textvariable=self.search_var, width=40).pack(side="left", padx=5)

        # --- Форма добавления/редактирования ---
        form_frame = LabelFrame(frame, text="Добавить/Редактировать клиента", padx=10, pady=10)
        form_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)

        Label(form_frame, text="Имя:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="Email:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.email_entry = Entry(form_frame, width=30)
        self.email_entry.grid(row=0, column=3, padx=5, pady=5)

        Label(form_frame, text="Телефон:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.phone_entry = Entry(form_frame, width=30)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(form_frame, text="Адрес:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.address_entry = Entry(form_frame, width=30)
        self.address_entry.grid(row=1, column=3, padx=5, pady=5)

        # Кнопки формы
        btn_frame = Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)

        self.save_btn = Button(btn_frame, text="Сохранить", command=self.save_client)
        self.save_btn.pack(side="left", padx=5)
        Button(btn_frame, text="Очистить", command=self.clear_fields).pack(side="left", padx=5)

        # --- Таблица клиентов ---
        table_frame = LabelFrame(frame, text="Клиенты", padx=10, pady=10)
        table_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Имя", "Email", "Телефон", "Адрес"),
            show="headings",
            height=15
        )

        columns = {
            "ID": "ID",
            "Имя": "name",
            "Email": "email",
            "Телефон": "phone",
            "Адрес": "address"
        }
        self.sort_columns = columns
        self.sort_reverse = {col: False for col in columns}

        for col, text in columns.items():
            self.tree.heading(col, text=text, command=lambda c=col: self.sort_by(c))
            self.tree.column(col, width=100 if col == "ID" else 150)

        scrollbar = Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.bind("<Double-1>", self.on_double_click)

        # --- Кнопки под таблицей ---
        action_btn_frame = Frame(frame)
        action_btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        Button(action_btn_frame, text="Обновить", command=self.load_clients).pack(side="left", padx=5)
        Button(action_btn_frame, text="Удалить выбранного", command=self.delete_client).pack(side="left", padx=5)
        Button(action_btn_frame, text="Экспорт в CSV", command=self.export_to_csv).pack(side="left", padx=5)
        Button(action_btn_frame, text="Выйти", command=self.window.destroy).pack(side="left", padx=5)

        self.current_client_id = None  # Для редактирования

        # Загрузка данных
        self.all_clients = []  # Хранит все данные для поиска и сортировки
        self.load_clients()

    def load_clients(self):
        """
        Загрузка всех клиентов из БД.
        """
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Clients")
            self.all_clients = cursor.fetchall()
            conn.close()
            self.display_clients(self.all_clients)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить клиентов: {e}")

    def display_clients(self, clients):
        """
        Отображение клиентов в таблице
        :param clients:
        :return:
        """
        for row in self.tree.get_children():
            self.tree.delete(row)
        for client in clients:
            self.tree.insert("", "end", values=client)

    def filter_clients(self, *args):
        """
        Поиск (фильтрация) клиентов
        :param args:
        :return:
        """
        term = self.search_var.get().lower()
        if not term:
            filtered = self.all_clients
        else:
            filtered = [
                c for c in self.all_clients
                if any(term in str(field).lower() for field in c)
            ]
        self.display_clients(filtered)

    def sort_by(self, col):
        """
        Сортировка по колонке при нажатии на заголовок колонки
        :param col:
        :return:
        """
        items = [(self.tree.set(child, col), child) for child in self.tree.get_children()]
        reverse = self.sort_reverse[col]
        items.sort(reverse=reverse)

        for index, (_, child) in enumerate(items):
            self.tree.move(child, "", index)

        self.sort_reverse[col] = not reverse

    def on_double_click(self, event):
        """
        Обработка двойного клика — редактирование
        :param event:
        :return:
        """
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item['values']
        client_id = values[0]

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])

        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, values[2])

        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, values[3])

        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, values[4] if values[4] else "")

        self.current_client_id = client_id
        self.save_btn.config(text="Обновить")

    def save_client(self):
        """
        Сохранение (добавление или обновление)
        :return:
        """
        client = Client

        client.name = self.name_entry.get().strip()
        client.email = self.email_entry.get().strip()
        client.phone = self.phone_entry.get().strip()
        client.address = self.address_entry.get().strip()

        try:
            conn = sqlite3.connect(DB_NAME)
            if self.current_client_id is None:
                # Добавление нового
                self.db.insert_client(
                    client.name,
                    client.email,
                    client.phone,
                    client.address)
                msg = "Клиент добавлен!"
            else:
                # Обновление существующего
                self.db.update_client(
                    client.name,
                    client.email,
                    client.phone,
                    client.address
                )
                msg = "Клиент обновлён!"
                self.clear_fields()  # Сбрасываем режим редактирования

            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", msg)
            self.load_clients()
            self.filter_clients()  # Применяем текущий фильтр
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить клиента: {e}")

    def delete_client(self):
        """
        Удаление клиента
        :return:
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Удаление", "Выберите клиента для удаления.")
            return

        item = self.tree.item(selected[0])
        client_id = item['values'][0]
        client_name = item['values'][1]

        if messagebox.askyesno("Подтверждение", f"Удалить клиента '{client_name}'?"):
            try:
                conn = sqlite3.connect(DB_NAME)
                self.db.delete_client(client_id)
                conn.commit()
                conn.close()
                messagebox.showinfo("Успех", "Клиент удалён.")
                self.load_clients()
                self.filter_clients()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить клиента: {e}")

    def export_to_csv(self):
        """
        Экспорт в CSV
        :return:
        """
        if not self.all_clients:
            messagebox.showinfo("Экспорт", "Нет данных для экспорта.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Сохранить как CSV"
        )
        if not file_path:
            return

        try:
            with open(file_path, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Имя", "Email", "Телефон", "Адрес"])
                writer.writerows(self.all_clients)
            messagebox.showinfo("Успех", f"Данные экспортированы в {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {e}")

    def clear_fields(self):
        """
        Очистка формы
        :return:
        """
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.current_client_id = None
        self.save_btn.config(text="Сохранить")

class ProductsWindow:
    """
    Окно управления товарами
    """
    def __init__(self, window):
        """
        Конструктор класса окна добавления товаров
        :param window:
        """
        self.window = window
        self.window.title("Товары")
        self.window.geometry("1000x600")
        self.db = Database()

        frame = Frame(self.window, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        # --- Поиск ---
        search_frame = Frame(frame)
        search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        Label(search_frame, text="Поиск:").pack(side="left", padx=5)
        self.search_var = StringVar()
        self.search_var.trace("w", self.filter_products)  # Live search
        Entry(search_frame, textvariable=self.search_var, width=40).pack(side="left", padx=5)

        # --- Форма добавления/редактирования ---
        form_frame = LabelFrame(frame, text="Добавить/Редактировать товар", padx=10, pady=10)
        form_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)

        Label(form_frame, text="Наименование:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="Цена").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.price_entry = Entry(form_frame, width=30)
        self.price_entry.grid(row=0, column=3, padx=5, pady=5)

        Label(form_frame, text="Количество:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.stock_entry = Entry(form_frame, width=30)
        self.stock_entry.grid(row=1, column=1, padx=5, pady=5)

        # Кнопки формы
        btn_frame = Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)

        self.save_btn = Button(btn_frame, text="Сохранить", command=self.save_product)
        self.save_btn.pack(side="left", padx=5)
        Button(btn_frame, text="Очистить", command=self.clear_fields).pack(side="left", padx=5)

        # --- Таблица товаров ---
        table_frame = LabelFrame(frame, text="Товары", padx=10, pady=10)
        table_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Наименование", "Цена", "Количество"),
            show="headings",
            height=15
        )

        # Заголовки и сортировка
        columns = {
            "ID": "ID",
            "Наименование": "name",
            "Цена": "price",
            "Количество": "stock",
        }
        self.sort_columns = columns
        self.sort_reverse = {col: False for col in columns}

        for col, text in columns.items():
            self.tree.heading(col, text=text, command=lambda c=col: self.sort_by(c))
            self.tree.column(col, width=100 if col == "ID" else 150)

        # Прокрутка
        scrollbar = Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Двойной клик для редактирования
        self.tree.bind("<Double-1>", self.on_double_click)

        # --- Кнопки под таблицей ---
        action_btn_frame = Frame(frame)
        action_btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        Button(action_btn_frame, text="Обновить", command=self.load_products).pack(side="left", padx=5)
        Button(action_btn_frame, text="Удалить", command=self.delete_product).pack(side="left", padx=5)
        Button(action_btn_frame, text="Экспорт в CSV", command=self.export_to_csv).pack(side="left", padx=5)
        Button(action_btn_frame, text="Выйти", command=self.window.destroy).pack(side="left", padx=5)

        self.current_product_id = None  # Для редактирования

        # Загрузка данных
        self.all_products = []  # Хранит все данные для поиска и сортировки
        self.load_products()

    def load_products(self):
        """
        Загрузка всех товаров из БД
        :return:
        """
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Products")
            self.all_products = cursor.fetchall()
            conn.close()
            self.display_products(self.all_products)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить товаров: {e}")

    def display_products(self, products):
        """
        Отображение товаров в таблице
        :param products:
        :return:
        """
        for row in self.tree.get_children():
            self.tree.delete(row)
        for product in products:
            self.tree.insert("", "end", values=product)

    def filter_products(self, *args):
        """
        Поиск (фильтрация)
        :param args:
        :return:
        """
        term = self.search_var.get().lower()
        if not term:
            filtered = self.all_products
        else:
            filtered = [
                c for c in self.all_products
                if any(term in str(field).lower() for field in c)
            ]
        self.display_products(filtered)

    def sort_by(self, col):
        """
        Сортировка по колонке, получаем индекс колонки,
        определяем, по какому полю сортировать (например, "Имя" -> "name"),
        перестраиваем строки, меняем направление для следующего клика
        :param col:
        :return:
        """
        items = [(self.tree.set(child, col), child) for child in self.tree.get_children()]
        reverse = self.sort_reverse[col]
        items.sort(reverse=reverse)

        for index, (_, child) in enumerate(items):
            self.tree.move(child, "", index)

        self.sort_reverse[col] = not reverse

    def on_double_click(self, event):
        """
        Обработка двойного клика — редактирование
        :param event:
        :return:
        """
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item['values']
        product_id = values[0]

        # Заполняем поля
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])

        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, values[2])

        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, values[3] if values[3] else "")

        # Сохранение ID для обновления
        self.current_product_id = product_id
        self.save_btn.config(text="Обновить")

    def save_product(self):
        """
        Сохранение (добавление или обновление)
        :return:
        """
        product = Product
        product.name = self.name_entry.get().strip()
        product.price = self.price_entry.get().strip()
        product.stock = self.stock_entry.get().strip()

        try:
            conn = sqlite3.connect(DB_NAME)
            if self.current_product_id is None:
                # Добавление нового
                self.db.insert_product(
                    Product.name,
                    Product.price,
                    Product.stock
                    )
                msg = "Товар добавлен!"
            else:
                # Обновление существующего
                self.db.update_product(
                    Product.name,
                    Product.price,
                    Product.stock
                    )
                msg = "Товар обновлён!"
                self.clear_fields()  # Сбрасываем режим редактирования

            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", msg)
            self.load_products()
            self.filter_products()  # Применяем текущий фильтр
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить товар: {e}")

    def delete_product(self):
        """
        Удаление товара
        :return:
        """
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Удаление", "Выберите товар для удаления.")
            return

        item = self.tree.item(selected[0])
        product_id = item['values'][0]
        product_name = item['values'][1]

        if messagebox.askyesno("Подтверждение", f"Удалить товар '{product_name}'?"):
            try:
                conn = sqlite3.connect(DB_NAME)
                self.db.delete_product(product_id)
                conn.commit()
                conn.close()
                messagebox.showinfo("Успех", "Товар удалён.")
                self.load_products()
                self.filter_products()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить товар: {e}")

    def export_to_csv(self):
        """
        Экспорт в CSV
        :return:
        """
        if not self.all_products:
            messagebox.showinfo("Экспорт", "Нет данных для экспорта.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Сохранить как CSV"
        )
        if not file_path:
            return
        try:
            with open(file_path, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Наименование", "Цена", "Количество"])
                writer.writerows(self.all_products)
            messagebox.showinfo("Успех", f"Данные экспортированы в {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {e}")

    def clear_fields(self):
        """
        Очистка формы
        :return:
        """
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.current_product_id = None
        self.save_btn.config(text="Сохранить")

class OrdersWindow:
    def __init__(self, window):
        """
        Конструктор класса окна управления заказами
        :param window:
        """
        self.window = window
        self.window.title("Заказы")
        self.window.geometry("800x600")
        self.db = Database()

        frame = Frame(self.window, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        # Поля выбора клиента и товара
        Label(frame, text="Клиент:").grid(row=0, column=0, sticky="w", pady=5)
        self.client_var = StringVar()
        self.client_combo = ttk.Combobox(frame, textvariable=self.client_var, state="readonly", width=30)
        self.client_combo.grid(row=0, column=1, pady=5)
        self.load_clients()

        Label(frame, text="Товар:").grid(row=1, column=0, sticky="w", pady=5)
        self.product_var = StringVar()
        self.product_combo = ttk.Combobox(frame, textvariable=self.product_var, state="readonly", width=30)
        self.product_combo.grid(row=1, column=1, pady=5)
        self.load_products()

        Label(frame, text="Количество:").grid(row=2, column=0, sticky="w", pady=5)
        self.quantity_entry = Entry(frame, width=30)
        self.quantity_entry.grid(row=2, column=1, pady=5)

        # Кнопки
        btn_frame = Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        Button(btn_frame, text="Сохранить", command=self.save_order).pack(side="left", padx=5)
        Button(btn_frame, text="Очистить", command=self.clear_fields).pack(side="left", padx=5)
        Button(btn_frame, text="Выйти", command=self.window.destroy).pack(side="left", padx=5)

        # Таблица заказов
        self.tree = ttk.Treeview(frame, columns=("ID", "Клиент", "Товар", "Кол-во", "Дата"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Клиент", text="Клиент")
        self.tree.heading("Товар", text="Товар")
        self.tree.heading("Кол-во", text="Кол-во")
        self.tree.heading("Дата", text="Дата")

        self.tree.column("ID", width=50)
        self.tree.column("Кол-во", width=70)
        self.tree.column("Дата", width=100)

        scrollbar = Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=4, column=2, sticky="ns")
        self.tree.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")

        frame.grid_rowconfigure(4, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        self.load_orders()

    def load_clients(self):
        """
        Загрузка клиентов из БД
        :return:
        """
        try:
            conn = sqlite3.connect(DB_NAME)
            clients = [f"{row[0]} - {row[1]}" for row in self.db.get_clients()]
            self.client_combo['values'] = clients
            conn.close()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить клиентов: {e}")

    def load_products(self):
        """
        Загрузка товаров из БД
        :return:
        """
        try:
            conn = sqlite3.connect(DB_NAME)
            products = [f"{row[0]} - {row[1]}" for row in self.db.get_products()]
            self.product_combo['values'] = products
            conn.close()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить товары: {e}")

    def load_orders(self):
        """
        Загрузка заказов из БД
        :return:
        """
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            conn = sqlite3.connect(DB_NAME)
            for row in self.db.get_orders():
                self.tree.insert("", "end", values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить заказы: {e}")

    def save_order(self):
        """
        Сохранение заказов в БД
        :return:
        """
        client_str = self.client_var.get()
        product_str = self.product_var.get()
        try:
            quantity = int(self.quantity_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть целым числом.")
            return

        if not client_str or not product_str or quantity <= 0:
            messagebox.showerror("Ошибка", "Все поля обязательны, количество > 0.")
            return

        Order.client_id = int(client_str.split(" - ")[0])
        Order.product_id = int(product_str.split(" - ")[0])
        Order.quantity = quantity
        Order.order_date = datetime.now().strftime("%Y-%m-%d")

        try:
            conn = sqlite3.connect(DB_NAME)
            self.db.insert_order(
                Order.client_id,
                Order.product_id,
                Order.quantity,
                Order.order_date
            )
            # cursor = conn.cursor()
            # cursor.execute("INSERT INTO Orders (client_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)",
            #                (client_id, product_id, quantity, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Заказ добавлен!")
            self.clear_fields()
            self.load_orders()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить заказ: {e}")

    def clear_fields(self):
        """
        Очистка полей
        :return:
        """
        self.client_var.set("")
        self.product_var.set("")
        self.quantity_entry.delete(0, tk.END)
