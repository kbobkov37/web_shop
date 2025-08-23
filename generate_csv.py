import csv
import random
from datetime import datetime, timedelta


# Генерация даты в пределах последних 30 дней
def random_date():
    start_date = datetime.now() - timedelta(days=30)
    random_days = random.randint(0, 30)
    return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')


# Открываем файл для записи
with open('orders.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Заголовки
    writer.writerow(['id', 'client_id', 'product_id', 'quantity', 'order_date'])

    # Генерация 100 записей
    for i in range(1, 1001):
        client_id = random.randint(1, 100)
        product_id = random.randint(1, 100)
        quantity = random.randint(1, 10)
        order_date = random_date()

        writer.writerow([i, client_id, product_id, quantity, order_date])

print("Файл orders.csv успешно создан с 100 заказами.")