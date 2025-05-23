from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv

# Initializing the lists for the Data fetches, Cambridge 2020 and 2019

PandemicNums = [None] * 13
PrePandiNums = [None] * 13

year = "2020"
for i in range(2, len(PandemicNums)+2):
    month = (i % 12) + 1
    print(f'{year}-{month:02}/{year}-{month:02}-cambridgeshire-outcomes.csv')
    PandemicNums[i-3] = len(pd.read_csv(Path(f'{year}-{month:02}/{year}-{month:02}-cambridgeshire-outcomes.csv')))
    if i >= 11:
        year = "2021"

year = "2019"
for i in range(2, len(PrePandiNums)+2):
    month = (i % 12) + 1
    print(f'{year}-{month:02}/{year}-{month:02}-cambridgeshire-outcomes.csv')
    PrePandiNums[i-3] = len(pd.read_csv(Path(f'{year}-{month:02}/{year}-{month:02}-cambridgeshire-outcomes.csv')))
    if i >= 11:
        year = "2020"

months = ("Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar")
x = np.arange(len(months))
width = 0.25

fig, ax = plt.subplots(layout='constrained')

black_olive = "#1F271B"
paynes_grey = "#19647E"
turquoise = "#28AFB0"
bg_color = "#efe6dd"

PrePandiCrimes = sum(PrePandiNums)
PandemicCrimes = sum(PandemicNums)
percHange = (PandemicCrimes-PrePandiCrimes)/PrePandiCrimes


print(f"The % in crime is {percHange*100}%")
ax.plot(x, PandemicNums, color=paynes_grey, marker='o', label="2020 to 2021", linewidth=3)
ax.plot(x, PrePandiNums, color=turquoise, marker='o', label="2019 to 2020", linewidth=3)

# Background colors
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# Labels and title
ax.set_ylabel("Crimes Reported", fontsize=20, fontweight = 'bold')
ax.set_title("Crimes during Pandemic vs Pre-Pandemic", fontsize=25, fontweight = 'bold')
ax.set_xticks(x)
ax.set_xticklabels(months, fontsize=14)
ax.tick_params(axis='y', labelsize=14)
ax.legend(loc="upper left", fontsize=18)

# Adjust Y axis
max_crimes = max(max(PandemicNums), max(PandemicNums))
ax.set_ylim(0, max_crimes * 1.5)

plt.show()