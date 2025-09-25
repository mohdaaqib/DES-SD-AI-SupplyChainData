import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = "mobile_sales_data.csv" 
sales_df = pd.read_csv(file_path, parse_dates=["Inward Date", "Dispatch Date"])


sales_df = sales_df[sales_df['Product'].str.contains("Mobile", na=False)]
sales_df['Dispatch Date'] = pd.to_datetime(sales_df['Dispatch Date'])

daily_demand = sales_df.groupby('Dispatch Date')['Quantity Sold'].sum().asfreq('D', fill_value=0)
weekly_demand = daily_demand.resample('W').sum()
k = 4  
alpha = 1.5
beta = 2.0
lead_time_weeks = 3

rolling_std = weekly_demand.rolling(window=k).std().fillna(0)
rolling_mean = weekly_demand.rolling(window=k).mean().fillna(0)

safety_stock = alpha * rolling_std + beta * lead_time_weeks
reorder_point = safety_stock + rolling_mean * lead_time_weeks

daily_rop = reorder_point.resample('D').ffill().reindex(daily_demand.index).fillna(method='bfill')

initial_inventory = 150
reorder_qty = 200
lead_time_days = lead_time_weeks * 7
days = len(daily_demand)
arrivals = [0] * (days + lead_time_days + 1)

inventory = []
stockouts = []
stock = initial_inventory

for t, demand in enumerate(daily_demand):
    stock += arrivals[t]
    if stock < daily_rop.iloc[t]:
        arrivals[t + lead_time_days] += reorder_qty
    fulfilled = min(stock, demand)
    stockout = max(0, demand - stock)
    stock = max(0, stock - fulfilled)
    stockouts.append(stockout)
    inventory.append(stock)

plt.figure(figsize=(14, 5))
plt.plot(daily_demand.index, daily_demand.values, label='Daily Demand', color='blue')
plt.plot(daily_demand.index, inventory, label='Inventory Level', color='orange')
plt.fill_between(daily_demand.index, 0, stockouts, color='red', alpha=0.3, label='Stockouts')
plt.plot(daily_demand.index, daily_rop.values, linestyle='--', color='gray', label='Dynamic ROP (from SD)')
plt.xlabel("Date")
plt.ylabel("Units")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
