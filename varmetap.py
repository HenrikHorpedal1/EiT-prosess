import numpy as np
import matplotlib.pyplot as plt

# Geometri og material
D1 = 60.3e-3  # m
D2 = 160e-3   # m
log = np.log(D2 / D1)
U = 0.1562  # W/mK (isolasjonsklasse 2)

# Temperaturer
T_indre = 65  # °C
T_ytre = np.linspace(-1, 5, 5)  # °C
delta_T = T_indre - T_ytre

# Varmetap per meter
Q_per_meter = 2 * np.pi * delta_T * U / log
print("Varmetap per meter [W/m]:", Q_per_meter, '\n')

# Totalt varmetap over 200 meter
L_total = 200
Q_total = Q_per_meter * L_total
print("Totalt varmetap [W]:", Q_total, '\n')

# Beregning av masseflow fra varmebehov
Q1 = 134  # kW
m_dot_kg_per_hour = Q1 * 860 / (65 - 50)  # kg/t
m_dot = m_dot_kg_per_hour / 3600  # kg/s

# Temperaturtap over 200 meter
c_p = 4180  # J/kgK
T_tap = Q_total / (m_dot * c_p)
print(f"Temperaturtap over 200 meter ved m_dot={m_dot:.3f} kg/s: {T_tap} °C \n")
plt.plot(T_ytre, Q_per_meter)
plt.xlabel("Omgivelsestemperatur [°C]")
plt.ylabel("Varmetap [W/m]")
plt.title("Varmetap per meter vs. omgivelsestemp")
plt.grid()
plt.show()
