import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter import messagebox, Toplevel, Label, Entry, Button, Frame, filedialog, StringVar
# import sqlite3
# import re
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from collections import Counter
from datetime import datetime
import os
import csv
from tkinter import *
from app import *
from db import Database
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
                         text="Управление интернет-магазином",
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
        self.window.geometry("1000x600")
        self.window.attributes("-topmost", True)
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
            self.tree.column(col, width=50 if col == "ID" else 150)

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
            self.all_clients = self.db.load_client()
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

        client.c_name = self.name_entry.get().strip()
        client.email = self.email_entry.get().strip()
        client.phone = self.phone_entry.get().strip()
        client.address = self.address_entry.get().strip()

        self.window.attributes("-topmost", False)

        try:
            if self.current_client_id is None:
                # Добавление нового
                self.db.insert_client(
                    client.c_name,
                    client.email,
                    client.phone,
                    client.address)
                msg = "Клиент добавлен!"
            else:
                # Обновление существующего
                self.db.update_client(
                    self.current_client_id,
                    client.c_name,
                    client.email,
                    client.phone,
                    client.address
                )
                msg = "Клиент обновлён!"
                self.clear_fields()

            messagebox.showinfo("Успех", msg)
            self.load_clients()
            self.filter_clients()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить клиента: {e}")

        self.window.attributes("-topmost", True)

    def delete_client(self):
        """
        Удаление клиента
        :return:
        """
        self.window.attributes("-topmost", False)
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Удаление", "Выберите клиента для удаления.")
            return

        item = self.tree.item(selected[0])
        client_id = item['values'][0]
        client_name = item['values'][1]

        if messagebox.askyesno("Подтверждение", f"Удалить клиента '{client_name}'?"):
            try:
                self.db.delete_client(client_id)
                messagebox.showinfo("Успех", "Клиент удалён.")
                self.load_clients()
                self.filter_clients()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить клиента: {e}")

        self.window.attributes("-topmost", True)

    def export_to_csv(self):
        """
        Экспорт в CSV
        :return:
        """
        self.window.attributes("-topmost", False)
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

        self.window.attributes("-topmost", False)

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
        self.window.attributes("-topmost", True)
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
            self.all_products = self.db.load_product()
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

        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, values[2])

        self.stock_entry.delete(0, tk.END)
        self.stock_entry.insert(0, values[3])

        # Сохранение ID для обновления
        self.current_product_id = product_id
        self.save_btn.config(text="Обновить")

    def save_product(self):
        """
        Сохранение (добавление или обновление)
        :return:
        """
        product = Product
        product.p_name = self.name_entry.get().strip()
        product.price = self.price_entry.get().strip()
        product.stock = self.stock_entry.get().strip()

        self.window.attributes("-topmost", False)

        try:
            if self.current_product_id is None:
                # Добавление нового
                self.db.insert_product(
                    product.p_name,
                    product.price,
                    product.stock
                    )
                msg = "Товар добавлен!"
            else:
                # Обновление существующего
                self.db.update_product(
                    self.current_product_id,
                    product.p_name,
                    product.price,
                    product.stock
                    )
                msg = "Товар обновлён!"
                self.clear_fields()  # Сбрасываем режим редактирования

            messagebox.showinfo("Успех", msg)
            self.load_products()
            self.filter_products()  # Применяем текущий фильтр
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить товар: {e}")

        self.window.attributes("-topmost", True)

    def delete_product(self):
        """
        Удаление товара
        :return:
        """
        self.window.attributes("-topmost", False)

        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Удаление", "Выберите товар для удаления.")
            return

        item = self.tree.item(selected[0])
        product_id = item['values'][0]
        product_name = item['values'][1]

        if messagebox.askyesno("Подтверждение", f"Удалить товар '{product_name}'?"):
            try:
                self.db.delete_product(product_id)
                messagebox.showinfo("Успех", "Товар удалён.")
                self.load_products()
                self.filter_products()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить товар: {e}")

            self.window.attributes("-topmost", True)

    def export_to_csv(self):
        """
        Экспорт в CSV
        :return:
        """
        self.window.attributes("-topmost", False)
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

        self.window.attributes("-topmost", True)

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
    """
    Окно управления заказами
    """
    def __init__(self, window):
        """
        Конструктор класса создания/редактирования новых заказов
        :param window:
        """
        self.window = window
        self.window.title("Заказы")
        self.window.geometry("1000x600")
        self.window.attributes("-topmost", True)
        self.db = Database()

        frame = Frame(self.window, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        # Поле поиска клиента и товара
        search_frame = Frame(frame)
        search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        Label(search_frame, text="Поиск:").pack(side="left", padx=5)
        self.search_var = StringVar()
        self.search_var.trace("w", self.filter_orders)  # Live search
        Entry(search_frame, textvariable=self.search_var, width=40).pack(side="left", padx=5)

        form_frame = LabelFrame(frame, text="Добавить/Редактировать заказ", padx=10, pady=10)
        form_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)

        # Поля выбора клиента и товара
        Label(form_frame, text="Клиент:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.client_var = StringVar()
        name_client = [cl[1] for cl in self.db.get_clients()]   # список для комбобокса
        self.client_combo = ttk.Combobox(
                                        form_frame,
                                        values=sorted(name_client),
                                        textvariable=self.client_var,
                                        state="readonly",
                                        width=30)
        self.client_combo.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="Товар:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.product_var = StringVar()
        name_product = [pr[1] for pr in self.db.get_products()]   # список для комбобокса
        self.product_combo = ttk.Combobox(
                                        form_frame,
                                        values=sorted(name_product),
                                        textvariable=self.product_var,
                                        state="readonly",
                                        width=30)
        self.product_combo.grid(row=1, column=1, padx=5, pady=5)

        Label(form_frame, text="Количество:").grid(row=0, column=3, sticky="w", padx=5, pady=5)
        self.quantity_entry = Entry(form_frame, width=30)
        self.quantity_entry.grid(row=0, column=4, padx=5, pady=5)

        Label(form_frame, text="Дата заказа:").grid(row=1, column=3, sticky="w", padx=5, pady=5)
        self.order_date_entry = DateEntry(
            form_frame,
            date_pattern="yyyy-mm-dd",
            width=30)
        self.order_date_entry.grid(row=1, column=4, padx=5, pady=5)

        # Кнопки формы
        btn_frame = Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)

        self.save_btn = Button(btn_frame, text="Сохранить", command=self.save_order)
        self.save_btn.pack(side="left", padx=5)
        Button(btn_frame, text="Очистить", command=self.clear_fields).pack(side="left", padx=5)

        # --- Таблица заказов ---
        table_frame = LabelFrame(frame, text="Заказы", padx=10, pady=10)
        table_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        frame.grid_rowconfigure(2, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Клиент", "Товар", "Кол-во", "Дата"),
            show="headings",
            height=15
        )

        columns = {
            "ID": "ID",
            "Клиент": "client_id",
            "Товар": "product_id",
            "Кол-во": "quantity",
            "Дата": "order_date"
        }
        self.sort_columns = columns
        self.sort_reverse = {col: False for col in columns}

        for col, text in columns.items():
            self.tree.heading(col, text=text, command=lambda c=col: self.sort_by(c))
            self.tree.column(col, width=50 if col == "ID" else 150)

        scrollbar = Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.bind("<Double-1>", self.on_double_click)

        # --- Кнопки под таблицей ---
        action_btn_frame = Frame(frame)
        action_btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        Button(action_btn_frame, text="Обновить", command=self.load_orders).pack(side="left", padx=5)
        Button(action_btn_frame, text="Удалить выбранного", command=self.delete_order).pack(side="left", padx=5)
        Button(action_btn_frame, text="Экспорт в CSV", command=self.export_to_csv).pack(side="left", padx=5)
        Button(action_btn_frame, text="Выйти", command=self.window.destroy).pack(side="left", padx=5)

        self.current_order_id = None  # Для редактирования

        # Загрузка данных
        self.all_orders = []  # Хранит все данные для поиска и сортировки
        self.load_orders()

    def load_orders(self):
        """
        Загрузка всех заказов из БД.
        """
        try:
            self.all_orders = self.db.load_order()
            self.display_orders(self.all_orders)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить заказы: {e}")

    def display_orders(self, orders):
        """
        Отображение заказов в таблице
        :param orders:
        :return:
        """
        for row in self.tree.get_children():
            self.tree.delete(row)
        for order in orders:
            self.tree.insert("", "end", values=order)

    def filter_orders(self, *args):
        """
        Поиск (фильтрация) заказов
        :param args:
        :return:
        """
        term = self.search_var.get().lower()
        if not term:
            filtered = self.all_orders
        else:
            filtered = [
                c for c in self.all_orders
                if any(term in str(field).lower() for field in c)
            ]
        self.display_orders(filtered)

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
        order_id = values[0]

        self.client_combo.delete(0, tk.END)
        self.client_combo.insert(0, values[1])

        self.product_combo.delete(0, tk.END)
        self.product_combo.insert(0, values[2])

        self.quantity_entry.delete(0, tk.END)
        self.quantity_entry.insert(0, values[3])

        self.order_date_entry.delete(0, tk.END)
        self.order_date_entry.insert(0, values[4] if values[4] else "")

        self.current_order_id = order_id
        self.save_btn.config(text="Обновить")

    def save_order(self):
        """
        Сохранение (добавление или обновление)
        :return:
        """
        self.window.attributes("-topmost", False)
        # client_str = self.client_var.get()
        # product_str = self.product_var.get()
        client_str = self.client_combo.get()
        product_str = self.product_combo.get()
        # client_str = self.client_var
        # product_str = self.product_var
        try:
            quantity = int(self.quantity_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть целым числом.")
            return

        if not client_str or not product_str or quantity <= 0:
            messagebox.showerror("Ошибка", "Все поля обязательны, количество > 0.")
            return
        print(f'{client_str=}, {product_str=}')
        pass
        order = Order
        order.client_id = self.db.get_client_id(client_str)
        order.product_id = self.db.get_product_id(product_str)
        order.quantity = quantity
        order.order_date = self.order_date_entry.get()
        # Order.order_date = datetime.now().strftime("%Y-%m-%d")

        try:
            # conn = sqlite3.connect(DB_NAME)
            self.db.insert_order(
                order.client_id,
                order.product_id,
                order.quantity,
                order.order_date
            )

            messagebox.showinfo("Успех", "Заказ добавлен!")
            self.clear_fields()
            self.load_orders()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить заказ: {e}")
            self.window.attributes("-topmost", True)

    def delete_order(self):
        """
        Удаление заказа
        :return:
        """
        self.window.attributes("-topmost", False)
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Удаление", "Выберите заказ для удаления.")
            return

        item = self.tree.item(selected[0])
        order_id = item['values'][0]
        # client_name = item['values'][1]

        if messagebox.askyesno("Подтверждение", f"Удалить заказ '{order_id}'?"):
            try:
                # conn = sqlite3.connect(DB_NAME)
                self.db.delete_order(order_id)
                messagebox.showinfo("Успех", "Заказ удалён.")
                self.load_orders()
                self.filter_orders()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить заказ: {e}")

            self.window.attributes("-topmost", True)

    def export_to_csv(self):
        """
        Экспорт в CSV
        :return:
        """
        if not self.all_orders:
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
                writer.writerow(["ID", "Клиент", "Товар", "Кол-во", "Дата"])
                writer.writerows(self.all_orders)
            messagebox.showinfo("Успех", f"Данные экспортированы в {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {e}")

    def clear_fields(self):
        """
        Очистка формы
        :return:
        """
        self.client_combo.delete(0, tk.END)
        self.product_combo.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.order_date_entry.delete(0, tk.END)
        self.current_order_id = None
        self.save_btn.config(text="Сохранить")

class StatsWindow:
    def __init__(self, window):
        """
        Конструктор класса статистики
        :param window:
        """
        self.window = window
        self.window.title("Статистика")
        self.window.geometry("1000x600")
        self.window.attributes("-topmost", True)
        self.db = Database()

        frame = Frame(self.window, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        # Создаем кнопки для выбора вида статистики
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=5)

        btn_top_clients = ttk.Button(button_frame,
                                     text="Топ-5 клиентов",
                                     command=self.show_top_5_clients)
        btn_orders_trend = ttk.Button(button_frame,
                                      text="Динамика заказов",
                                      command=self.show_orders_trend)
        btn_graph_clients_products = ttk.Button(button_frame,
                                                text="Граф связей",
                                                command=self.show_clients_products_graph)
        btn_exit = ttk.Button(button_frame,
                              text="Выйти",
                              command=self.window.destroy)

        btn_top_clients.pack(side='left',
                             padx=5)
        btn_orders_trend.pack(side='left',
                              padx=5)
        btn_graph_clients_products.pack(side='left',
                                        padx=5)
        btn_exit.pack(side='left',
                      padx=5)

        self.chart_frame = ttk.LabelFrame(frame, text="Статистика")
        self.chart_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.current_canvas = None

    def clear_chart(self):
        # Удаляем предыдущий график, если есть
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
            self.current_canvas = None

    def show_top_5_clients(self):
        self.clear_chart()

        results = self.db.top_5_client()
        names = [row[1] for row in results]
        counts = [row[2] for row in results]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.barh(names, counts)
        ax.set_xlabel('Количество заказов')
        ax.set_title('Топ-5 клиентов по заказам')
        ax.invert_yaxis()

        self.current_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().pack(fill='both', expand=True)

    def show_orders_trend(self):
        self.clear_chart()

        results = self.db.show_order_trend()
        dates = [row[0] for row in results]
        counts = [row[1] for row in results]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(dates, counts, marker='o')
        ax.set_xlabel('Дата заказа')
        ax.set_ylabel('Количество заказов')
        ax.set_title('Динамика заказов по датам')

        plt.setp(ax.get_xticklabels(), rotation=45)

        self.current_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().pack(fill='both', expand=True)

    def show_clients_products_graph(self):
        """
        Строим граф связей клиентов и продуктов
        :return:
        """
        self.clear_chart()

        G = nx.Graph()

        edges = self.db.show_client_product_graph()

        clients = set([row[0] for row in edges])
        products = set([row[1] for row in edges])

        G.add_nodes_from(clients, type='client')
        G.add_nodes_from(products, type='product')

        for client_name, product_name in edges:
            G.add_edge(client_name, product_name)

        pos = nx.spring_layout(G)

        fig, ax = plt.subplots(figsize=(8, 6))

        client_nodes = [n for n, attr in G.nodes(data=True) if attr['type'] == 'client']
        product_nodes = [n for n, attr in G.nodes(data=True) if attr['type'] == 'product']

        nx.draw_networkx_nodes(G, pos,
                               nodelist=client_nodes,
                               node_color='lightblue',
                               node_size=500,
                               label='Клиенты',
                               ax=ax)

        nx.draw_networkx_nodes(G, pos,
                               nodelist=product_nodes,
                               node_color='lightgreen',
                               node_size=500,
                               label='Продукты',
                               ax=ax)

        nx.draw_networkx_edges(G, pos, ax=ax)

        nx.draw_networkx_labels(G, pos, ax=ax)

        # Легенда вручную через Patch или Line2D объекты
        import matplotlib.patches as mpatches
        legend_handles = [
            mpatches.Patch(color='lightblue', label='Клиенты'),
            mpatches.Patch(color='lightgreen', label='Продукты')
        ]
        ax.legend(handles=legend_handles)

        ax.set_title('Граф связей клиентов и продуктов')
        ax.axis('off')

        self.current_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().pack(fill='both', expand=True)
