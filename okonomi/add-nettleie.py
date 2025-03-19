import pandas as pd

nettleie = 20 #øre
df = pd.read_csv("interpolated_power_prices.csv")
df[["High", "Base", "Low"]] = df[["High", "Base", "Low"]] + nettleie

df.to_csv("interpolated_power_prices_with_nettleie.csv", index = False)




