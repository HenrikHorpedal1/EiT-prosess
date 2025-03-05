import numpy as np
import numpy_financial as npf  # For IRR calculation
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style for better visuals
sns.set_style("whitegrid")

# === Project Parameters (in NOK) ===
total_project_cost = -3_122_847  # Total capital cost (NOK) from SINTEF
funding_amount = 800_00  # Same as Enova example as for now
initial_investment = total_project_cost + funding_amount  # Adjusted investment needed from the company

annual_revenue = 0  # Heat sales revenue (NOK/year)
annual_operating_cost = -initial_investment * 0.01  # Maintenance & operation costs (NOK/year), same assumption as Sintef
project_lifetime = 20  # Years
discount_rate = 0.06  # 6% discount rate

# === Energy Savings Due to Community Heating ===
annual_energy_saved_mwh = 500  # Megawatt-hours (MWh) saved per year
energy_price_per_mwh = 740  # Cost per MWh in NOK (e.g., electricity/gas cost)
annual_energy_savings = annual_energy_saved_mwh * energy_price_per_mwh  # Total savings in NOK

# === Compute Cash Flow Adjusted with Energy Savings ===
annual_cash_flow = (annual_revenue + annual_energy_savings) - annual_operating_cost
cash_flows = [initial_investment] + [annual_cash_flow] * project_lifetime

# === Financial Calculations ===
years = np.arange(0, project_lifetime + 1)
discounted_cash_flows = [cf / (1 + discount_rate) ** t for t, cf in enumerate(cash_flows)]
npv = sum(discounted_cash_flows)
irr = npf.irr(cash_flows)
cumulative_cash_flow = np.cumsum(cash_flows)
payback_period = np.where(cumulative_cash_flow > 0)[0][0]  # First year when cash flow turns positive
total_benefits = sum(discounted_cash_flows[1:])  # Excluding initial investment
bcr = total_benefits / abs(initial_investment)

# === Print Results (in NOK) ===
print(f"Total Project Cost: {total_project_cost:,.0f} NOK")
print(f"Funding Amount: {funding_amount:,.0f} NOK")
print(f"Net Investment Needed: {initial_investment:,.0f} NOK")
print(f"Net Present Value (NPV): {npv:,.0f} NOK")
print(f"Internal Rate of Return (IRR): {irr:.2%}")
print(f"Payback Period: {payback_period} years")
print(f"Benefit-Cost Ratio (BCR): {bcr:.2f}")
print(f"Annual Energy Savings: {annual_energy_savings:,.0f} NOK")

# === Visualization 1: Cumulative Cash Flow Over Time ===
plt.figure(figsize=(10, 5))
plt.bar(years, cumulative_cash_flow, color="royalblue", alpha=0.7)
plt.axhline(0, color="black", linestyle="--")
plt.xlabel("Year")
plt.ylabel("Cumulative Cash Flow (NOK)")
plt.title("Payback Period & Cash Flow Over Time")
plt.annotate(f"Break-even at Year {payback_period}", 
             xy=(payback_period, 0), 
             xytext=(payback_period - 3, max(cumulative_cash_flow) * 0.1),
             arrowprops=dict(arrowstyle="->", color="red"),
             fontsize=12, color="red")
plt.show()

# === Visualization 2: Energy Savings Impact Over Time ===
plt.figure(figsize=(10, 5))
total_energy_savings = np.array([annual_energy_savings] * project_lifetime).cumsum()
plt.plot(years[1:], total_energy_savings, marker="o", linestyle="-", color="green", label="Cumulative Energy Savings (NOK)")
plt.axhline(0, color="black", linestyle="--")
plt.xlabel("Year")
plt.ylabel("Cumulative Savings (NOK)")
plt.title("Cumulative Energy Cost Savings Over Time")
plt.legend()
plt.grid(True)
plt.show()

