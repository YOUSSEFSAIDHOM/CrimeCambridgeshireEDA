from IPython import display
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Initializing the lists for the Data fetches, Cambridge 2020 and 2019

DataFetch_PAN = [None] * 13
DataFetch_PREPAN= [None] * 13

months = ("Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar")
month = 0

for i in range(len(months)):
    month = months.index(months[i % 11])
    print(month + 1)
    year = "2020"
    DataFetch_PAN[i] = len(pd.read_csv(Path(f'{year}-{month+1:02}/{year}-{month+1:02}-cambridgeshire-outcomes.csv')))
    if months[month] == "Dec":
        year = "2021"

for j in range(len(months)):
    month = months.index(months[j % 11])
    year = "2019"
    DataFetch_PREPAN[j] = len(pd.read_csv(Path(f'{year}-{month+1:02}/{year}-{month+1:02}-cambridgeshire-outcomes.csv')))
    if months[month] == "Dec":
        year = "2020"

crimes_pan = [DataFetch_PAN[i] for i in range(len(months))]
crimes_pre = [DataFetch_PREPAN[i] for i in range(len(months))]

x = np.arange(len(months))
width = 0.25

fig, ax = plt.subplots(layout='constrained')

# Colours
black_olive = "#1F271B"
paynes_grey = "#19647E"
turquoise = "#28AFB0"
bg_color = "#efe6dd"

# Plotting lines
ax.plot(x, crimes_pre, color=black_olive, marker='o', label="Crime levels before the pandemic", linewidth=3)
ax.plot(x, crimes_pan, color=turquoise, marker='o', label="Crime levels during pandemic", linewidth=3)

# Background colors
fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

# Labels and title
ax.set_ylabel("Crimes Reported", fontsize=10, fontweight='bold', labelpad=20)
ax.set_title("Crimes in Cambridgeshire, pre pandemic vs post pandemic", fontsize=15, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(months, fontsize=14)
ax.tick_params(axis='y', labelsize=14)
ax.legend(loc="upper left", fontsize=18)

plt.show()