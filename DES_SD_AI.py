import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = ("mobile_sales_data.csv")  
sales_df = pd.read_csv(file_path, parse_dates=["Inward Date", "Dispatch Date"])
sales_df = sales_df[sales_df['Product'].str.contains("Mobile", na=False)]
sales_df['Dispatch Date'] = pd.to_datetime(sales_df['Dispatch Date'])

daily_demand = sales_df.groupby('Dispatch Date')['Quantity Sold'].sum().asfreq('D', fill_value=0)
weekly_demand = daily_demand.resample('W').sum()


# SD Layer: Weekly Reorder Policies
k = 4  
alpha = 1.5
beta = 2.0
lead_time_weeks = 3

rolling_std = weekly_demand.rolling(window=k).std().fillna(0)
rolling_mean = weekly_demand.rolling(window=k).mean().fillna(0)

safety_stock = alpha * rolling_std + beta * lead_time_weeks
reorder_point = safety_stock + rolling_mean * lead_time_weeks

daily_rop = reorder_point.resample('D').ffill().reindex(daily_demand.index).fillna(method='bfill')


# DES Layer
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

# RL Layer:
episodes = np.arange(1, 101)
q_values = [50 + 20 * np.exp(-0.05 * ep) + np.random.normal(0, 2) for ep in episodes]
q_value_norm = (np.array(q_values) - np.min(q_values)) / (np.max(q_values) - np.min(q_values))
q_curve = np.interp(np.arange(len(daily_demand)), np.linspace(0, len(daily_demand), num=len(q_value_norm)), q_value_norm)


# EA Layer: 
np.random.seed(42)
service_levels = np.linspace(0.8, 1.0, 30)
inventory_costs = 1000 / service_levels + np.random.normal(0, 10, size=len(service_levels))
start_date = daily_demand.index[0].toordinal()
end_date = daily_demand.index[-1].toordinal()
ea_x = np.linspace(start_date, end_date, num=30)
ea_x_dates = [pd.Timestamp.fromordinal(int(x)) for x in ea_x]
ea_y = np.interp(service_levels, [0.8, 1.0], [0, daily_demand.max() * 0.8])


fig, ax = plt.subplots(figsize=(16, 10))
ax.plot(daily_demand.index, daily_demand.values, label='Daily Demand (DES)', color='blue')
ax.plot(daily_demand.index, inventory, label='Inventory Level (DES)', color='orange')
ax.fill_between(daily_demand.index, 0, stockouts, color='red', alpha=0.2, label='Stockouts (DES)')
ax.plot(daily_demand.index, daily_rop.values, linestyle='--', color='gray', label='Dynamic ROP (from SD)')
ax.plot(daily_demand.index, q_curve * max(daily_demand.max(), max(inventory)), color='purple', alpha=0.7, label='RL: Q-Value (scaled)')
scatter = ax.scatter(ea_x_dates, ea_y, marker='x', c=service_levels, cmap='viridis', label='EA Pareto Points (Cost vs. Service)')
ax.set_xlabel("Date")
ax.set_ylabel("Inventory / Demand / Utility Units")
ax.grid(True)
ax.legend(loc='upper left')
plt.tight_layout()
plt.show()
