import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

random.seed(42)
np.random.seed(42)

# -----------------------------
# Настройки
# -----------------------------

ORDERS = 20000
CUSTOMERS = 500

os.makedirs("data", exist_ok=True)


# -----------------------------
# Справочники магазина
# -----------------------------

cities = [
    "Moscow",
    "Saint Petersburg",
    "Kazan",
    "Ufa",
    "Novosibirsk",
    "Yekaterinburg",
    "Samara",
    "Perm",
    "Voronezh"
]

city_weights = [
    30, 20, 10, 8, 8, 8, 6, 5, 5
]


products = [
    ("Smartphone", "iPhone 15", 89990),
    ("Smartphone", "Samsung Galaxy S24", 74990),
    ("Smartphone", "Xiaomi 14", 54990),

    ("Laptop", "MacBook Air M3", 139990),
    ("Laptop", "Lenovo IdeaPad", 69990),
    ("Laptop", "ASUS VivoBook", 64990),

    ("Headphones", "AirPods Pro", 24990),
    ("Headphones", "Sony WH-1000XM5", 32990),
    ("Headphones", "JBL Tune", 4990),

    ("Monitor", "LG UltraWide", 34990),
    ("Monitor", "Samsung Odyssey", 45990),

    ("Tablet", "iPad Air", 69990),
    ("Tablet", "Xiaomi Pad 6", 34990),

    ("Smartwatch", "Apple Watch", 49990),
    ("Smartwatch", "Galaxy Watch", 32990)
]


payments = [
    "Card",
    "SBP",
    "Cash"
]


# -----------------------------
# Клиенты
# -----------------------------

customers = pd.DataFrame({
    "CustomerID": range(1, CUSTOMERS + 1),
    "City": np.random.choice(
        cities,
        CUSTOMERS,
        p=np.array(city_weights)/sum(city_weights)
    )
})


# -----------------------------
# Генерация заказов
# -----------------------------

rows = []

start_date = datetime(2025, 1, 1)

for order_id in range(1, ORDERS + 1):

    customer = customers.sample(1).iloc[0]

    # дата
    date = start_date + timedelta(
        days=random.randint(0, 364)
    )

    month = date.month


    # выбираем товар
    category, product, price = random.choice(products)


    # сезонность
    season_factor = 1

    if month in [11, 12]:
        season_factor = 1.8

    if month in [8, 9]:
        if category in ["Laptop", "Tablet"]:
            season_factor = 1.5


    # количество товара
    if category in ["Headphones", "Smartwatch"]:
        quantity = random.choice([1, 1, 1, 2])
    else:
        quantity = 1


    # скидка
    if month == 11:
        discount = random.choice(
            [10, 15, 20, 25]
        )
    else:
        discount = random.choice(
            [0, 0, 5, 10]
        )


    # способ оплаты
    if price > 50000:
        payment = random.choices(
            payments,
            weights=[75,20,5]
        )[0]
    else:
        payment = random.choices(
            payments,
            weights=[60,25,15]
        )[0]


    revenue = (
        price *
        quantity *
        (1 - discount / 100)
    )


    rows.append([
        order_id,
        customer["CustomerID"],
        date.date(),
        customer["City"],
        category,
        product,
        price,
        quantity,
        discount,
        payment,
        round(revenue, 2)
    ])


# -----------------------------
# Создаем DataFrame
# -----------------------------

df = pd.DataFrame(
    rows,
    columns=[
        "OrderID",
        "CustomerID",
        "Date",
        "City",
        "Category",
        "Product",
        "Price",
        "Quantity",
        "Discount",
        "Payment",
        "Revenue"
    ]
)


# сохраняем

df.to_csv(
    "data/sales.csv",
    index=False
)


print("Dataset created!")
print(df.head())
print()
print("Rows:", len(df))