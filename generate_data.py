import pandas as pd
import random
from datetime import datetime, timedelta

categories = ["Food", "Travel", "Shopping", "Bills", "Entertainment"]

start_date = datetime(2024, 1, 1)

data = []

for i in range(300):

    date = start_date + timedelta(days=i)

    category = random.choice(categories)

    amount = random.randint(100, 3000)

    data.append([date.strftime("%Y-%m-%d"), category, amount])

df = pd.DataFrame(data, columns=["date", "category", "amount"])

df.to_csv("data/expenses.csv", index=False)

print("300 rows dataset created successfully!")