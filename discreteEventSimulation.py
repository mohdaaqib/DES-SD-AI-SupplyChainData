import pandas as pd
import matplotlib.pyplot as plt

file_path = ("mobile_sales_data.csv") # dataset loading 
sales_df = pd.read_csv(file_path, parse_dates=["Inward Date", "Dispatch Date"])

# in belowe we Filter mobile products and prepare dates
sales_df = sales_df[sales_df['Product'].str.contains("Mobile", na=False)]
sales_df['Dispatch Date'] = pd.to_datetime(sales_df['Dispatch Date'])
sales_df['Inward Date'] = pd.to_datetime(sales_df['Inward Date'])

# This creates daily demand series
daily_demand = sales_df.groupby('Dispatch Date')['Quantity Sold'].sum().asfreq('D', fill_value=0)

# Below are some DES simulation parameters
initial_inventory = 150
reorder_point = 100
reorder_qty = 200
lead_time = 3
days = len(daily_demand)
arrivals = [0] * (days + lead_time + 1)

inventory = []
stock = initial_inventory
stockouts = []

# Simulation runs from here
for t, demand in enumerate(daily_demand):
    stock += arrivals[t]
    if stock < reorder_point:
        arrivals[t + lead_time] += reorder_qty
    fulfilled = min(stock, demand)
    stockouts.append(max(0, demand - stock))
    stock = max(0, stock - fulfilled)
    inventory.append(stock)

# Plot the result
plt.figure(figsize=(12, 6))
plt.plot(daily_demand.index, daily_demand.values, label='Daily Demand')
plt.plot(daily_demand.index, inventory, label='Inventory Level')
plt.fill_between(daily_demand.index, stockouts, label='Stockouts', color='red', alpha=0.3)
plt.axhline(reorder_point, color='gray', linestyle='--', label='Reorder Point')
# plt.title('DES Simulation: Mobile Sales Inventory vs. Demand')
plt.xlabel('Date')
plt.ylabel('Units')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
