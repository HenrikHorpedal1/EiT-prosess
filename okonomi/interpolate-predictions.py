import numpy as np
import pandas as pd

def interpolate_and_save():
    # Define known years and values for each scenario
    years = np.array([2030, 2035, 2040, 2050])
    base_values = np.array([81, 59, 51, 46])
    low_values = np.array([47, 34, 28, 30])
    high_values = np.array([121, 84, 77, 64])
    
    # Generate yearly range
    all_years = np.arange(2030, 2051)  # From 2030 to 2050, inclusive
    
    # Perform linear interpolation
    base_interp = np.interp(all_years, years, base_values)
    low_interp = np.interp(all_years, years, low_values)
    high_interp = np.interp(all_years, years, high_values)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Year': all_years,
        'Base': base_interp,
        'Low': low_interp,
        'High': high_interp
    })

    print(df)
    
    # Save to CSV
    df.to_csv('extrapolated_power_prices.csv', index=False)
    
    print("CSV file 'extrapolated_power_prices.csv' saved successfully.")

# Run the function
interpolate_and_save()
