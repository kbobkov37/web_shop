# 🛒 Интернет-магазин — Управление и статистика

Простое приложение для управления интернет-магазином с графическим интерфейсом на **Tkinter**, базой данных **SQLite** и визуализацией статистики. Позволяет управлять клиентами, товарами, заказами и просматривать аналитику.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Основные функции

- **Управление клиентами**: добавление, редактирование, удаление, поиск.
- **Управление товарами**: контроль остатков и цен.
- **Управление заказами**: оформление, просмотр, удаление.
- **Статистика и аналитика**:
  - Топ-5 клиентов по заказам
  - Динамика заказов по датам
  - Граф связей клиентов и товаров
- **Экспорт данных** в CSV
- **Автоматическая валидация** данных (email, телефон, цена и т.д.)
- Полное **юнит-тестирование** и **документация Sphinx**

---

## 🖼 Скриншоты интерфейса

### Главное окно
![Main App](docs/_images/main_app.png)

### Управление клиентами
![Clients](docs/_images/client.png)
![Clients](docs/_images/client_search.png)
![Clients](docs/_images/client_sort.png)
![Clients](docs/_images/client_d-clck.png)

### Статистика: 
####Топ-5 клиентов по заказам
![Stats](docs/_images/stat_top-5.png)
####Динамика заказов по датам
![Stats](docs/_images/dyn_orders.png)
####Граф связей клиентов и товаров
![Stats](docs/_images/graph_top-50.png)

> 💡 *Примечание: Чтобы добавить реальные изображения, поместите скриншоты в папку `docs/_images/` и обновите пути.*

---

## 🚀 Быстрый запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/ваше-имя/online-store-app.git
cd online-store-app