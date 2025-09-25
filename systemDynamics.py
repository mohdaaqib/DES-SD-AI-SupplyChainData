import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file_path = ("mobile_sales_data.csv") # dataset loading 
sales_df = pd.read_csv(file_path, parse_dates=["Inward Date", "Dispatch Date"])

# Filter mobile products
sales_df = sales_df[sales_df['Product'].str.contains("Mobile", na=False)]

# Aggregate demands based on weekly 
sales_df['Dispatch Date'] = pd.to_datetime(sales_df['Dispatch Date'])
weekly_demand = sales_df.groupby(pd.Grouper(key='Dispatch Date', freq='W'))['Quantity Sold'].sum().fillna(0)

# Compute the rolling volatility and adaptive safety stock
k = 4  # 4-week window
alpha = 1.5
beta = 2.0
lead_time = 3  # Assume average lead time of 3 weeks

rolling_std = weekly_demand.rolling(window=k).std().fillna(0)
safety_stock = alpha * rolling_std + beta * lead_time
reorder_point = safety_stock + weekly_demand.rolling(window=k).mean().fillna(0) * lead_time

weekly_demand_values = weekly_demand.values.astype(float)
safety_stock_values = safety_stock.values.astype(float)
reorder_point_values = reorder_point.values.astype(float)

plt.figure(figsize=(12, 6))
plt.plot(weekly_demand.index, weekly_demand_values, label='Weekly Demand')
plt.plot(weekly_demand.index, safety_stock_values, label='Safety Stock (SS)', linestyle='--')
plt.plot(weekly_demand.index, reorder_point_values, label='Reorder Point (ROP)', linestyle='-.')
plt.fill_between(weekly_demand.index, safety_stock_values, reorder_point_values, color='orange', alpha=0.2, label='Buffer Zone')
plt.xlabel("Week")
plt.ylabel("Units")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
