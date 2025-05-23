from IPython import display
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv

months = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

dfraw = pd.read_csv("STOP_SEARCH_2020.csv")
crime_dict = {}
for i in range(5):
    crime_dict[dfraw.iloc[i,0]] = [dfraw.iloc[i,j] for j in range(1,len(months)+1)]

bg_color = "#efe6dd"

colours = ["#1F271B", "#19647E", "#28AFB0", "#F4D35E", "#EE964B"]

x = np.arange(len(months))
width = 0.5

fig, ax = plt.subplots()
bottom = np.zeros(len(months))

for idx, (boolean, crime) in enumerate (crime_dict.items()):
    color = colours[idx % len(colours)]
    p = ax.bar(x, crime, width, label=boolean, bottom=bottom, color = color)
    bottom += crime

fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

ax.set_ylabel("Stop searches", fontsize=10, fontweight = 'bold')
ax.set_title("Reason of stop searches in 2020", fontsize=15, fontweight='bold')
ax.set_xticks(x)
plt.xticks(rotation=30)
ax.set_xticklabels(months, fontsize=14)
ax.tick_params(axis='y', labelsize=14)
ax.legend(loc="upper left", fontsize=14)

plt.show()
