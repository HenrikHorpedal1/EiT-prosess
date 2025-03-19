import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy_financial as npf  # For IRR calculation

# --- Project Financial & Energy Parameters ---
total_project_cost = -3_122_847  # from SINTEF
funding_amount = 800_000  
initial_investment = total_project_cost + funding_amount 
annual_operating_cost = -initial_investment * 0.01  # Operating cost (1% of investment)
project_lifetime = 20  # Years of operation (after initial investment)

# Electricity
annual_electrical_energy_saved_mwh = 500  
df_prices = pd.read_csv("interpolated_power_prices.csv")
start_year = df_prices['Year'].iloc[0]  # e.g., 2030
# Assume initial investment occurs in start_year, and operating cash flows start the following year.
# Filter to get the next 'project_lifetime' years for operating cash flows.
df_operating = df_prices[df_prices['Year'] > start_year].iloc[:project_lifetime]
# Convert the "Base" price from øre/kWh to NOK/MWh (1 øre/kWh = 10 NOK/MWh)
electricity_prices_nok_per_mwh = df_operating['High'].values * 10

#Gas
annual_gas_energy_saved_mwh = 0
gas_price_per_mwh = 0

# --- Read CSV Data ---
df_prices = pd.read_csv("interpolated_power_prices.csv")
start_year = df_prices['Year'].iloc[0]  # e.g., 2030

# Assume initial investment occurs in start_year, and operating cash flows start the following year.
# Filter to get the next 'project_lifetime' years for operating cash flows.
df_operating = df_prices[df_prices['Year'] > start_year].iloc[:project_lifetime]

# Convert the "Base" price from øre/kWh to NOK/MWh (1 øre/kWh = 10 NOK/MWh)
electricity_prices_nok_per_mwh = df_operating['High'].values * 10

# --- Calculate Annual Energy Savings ---
annual_energy_savings = (annual_electrical_energy_saved_mwh * electricity_prices_nok_per_mwh +
                         annual_gas_energy_saved_mwh * gas_price_per_mwh)

# --- Calculate Cash Flows ---
# Operating cash flow = energy savings minus annual operating cost.
annual_cash_flow = annual_energy_savings - annual_operating_cost

# The full cash flow array: initial investment (year 0) plus operating cash flows for the project lifetime.
cash_flows = [initial_investment] + list(annual_cash_flow)

# --- Create a Time Array ---
# There will be 1 (investment) + project_lifetime cash flows.
years = np.arange(0, project_lifetime + 1)  # e.g., 0 through 20 (21 points)

# --- Compute Cumulative Cash Flow and Payback Period ---
cumulative_cash_flow = np.cumsum(cash_flows)
indices = np.where(cumulative_cash_flow > 0)[0]
if indices.size > 0:
    payback_period = indices[0]
    print(f"Break-even at Year {payback_period}")
else:
    print("The project never reaches break-even within the project lifetime.")

# --- Plot the Cash Flow ---
plt.figure(figsize=(10, 5))
plt.bar(years, cumulative_cash_flow, color="royalblue", alpha=0.7)
plt.axhline(0, color="black", linestyle="--")
plt.xlabel("Year")
plt.ylabel("Cumulative Cash Flow (NOK)")
plt.title("Payback Period & Cash Flow Over Time")
if indices.size > 0:
    plt.annotate(f"Break-even at Year {payback_period}", 
                 xy=(payback_period, 0), 
                 xytext=(payback_period - 3, max(cumulative_cash_flow) * 0.1),
                 arrowprops=dict(arrowstyle="->", color="red"),
                 fontsize=12, color="red")
plt.show()

# --- Calculate IRR ---
irr = npf.irr(cash_flows)
print("IRR: ", irr)

