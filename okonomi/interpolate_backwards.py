import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

start_year = 2024
average_power_price_2024 = 74 #øre/kWh Fra sintef rapport
df_2024 = pd.DataFrame({
    "Year": [2024],
    "Base": [average_power_price_2024],
    "Low": [average_power_price_2024],
    "High": [average_power_price_2024]
})


interpolated_power_predictions_with_nettleie = pd.read_csv("interpolated_power_prices_with_nettleie.csv")
df_all = pd.concat([df_2024, interpolated_power_predictions_with_nettleie], ignore_index=True)
df_all = df_all.sort_values("Year").reset_index(drop=True)
df_all.set_index("Year", inplace=True)
new_index = np.arange(df_all.index.min(), df_all.index.max() + 1)
df_all = df_all.reindex(new_index)

# --- Interpolate Linearly ---
df_all = df_all.interpolate(method="linear")



# Plot the lines

plt.figure(figsize=(10, 6))
plt.plot(df_all.index, df_all['Base'], linestyle='--', linewidth=2.0, label='Grunntilfelle')
plt.plot(df_all.index, df_all['High'], linestyle='--', linewidth=2.0, label='Høy')
plt.plot(df_all.index, df_all['Low'], linestyle='--', linewidth=2.0, label='Lav')

marker_size = 60  # Adjust this value to change the marker size
# Mark the starting point for "Base" with a red dot on top (using zorder to ensure it's on top)
start_year = df_all.index.min()
plt.scatter(start_year, df_all.loc[start_year, 'Base'], color='red', s=marker_size, label='Verdalskalks gjennomsnittlige strømpris 2024', zorder=10)

# Shade the area from 2024 to 2030 in gray with a label
#plt.axvspan(2024, 2030, color='gray', alpha=0.2, label='Interpolert område')

# Add placeholder text (positioned at x=2025 and near the top of the "Base" data)
#plt.text(2025, df_all['Base'].max(), 'Placeholder Text', fontsize=12, color='black')

# Define special years and add markers on all three lines
special_years = [2030, 2035, 2040, 2050]

# Plot special markers (using the same color for all three series)
plt.scatter(special_years, df_all.loc[special_years, 'Base'], color='gray', s=marker_size, label='Prediksjoner fra NVE med pålagt 20kr nettleie', zorder=10)
plt.scatter(special_years, df_all.loc[special_years, 'High'], color='gray', s=marker_size, zorder=10)
plt.scatter(special_years, df_all.loc[special_years, 'Low'], color='gray', s=marker_size, zorder=10)

# Add labels, grid, and legend
plt.title('Interpolerte strømprisprediksjoner inkludert nettleie')
plt.xlabel('År')
plt.ylabel('Øre/kWh')
plt.grid(True)
plt.legend()

# Display the plot
plt.show()

