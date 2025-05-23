import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

#  Anti-social behaviour, Cambridgeshire vs Nationally

colours = ["#1F271B", "#19647E", "#28AFB0", "#F4D35E", "#EE964B"]
bg_color = "#efe6dd"

national = pd.read_csv('National_Crime_Recs_PM_(ALL_TYPES).csv')
local = pd.read_csv('Crime_Cambridgeshire.csv')

combined = national.merge(local, left_on='Month', right_on='Month')
combined_months = combined.set_index('Month')

national_records = combined['Records']
local_crimes = combined['Crimes']

fig, ax1 = plt.subplots()
x = np.arange(len(combined_months.index))

fig.patch.set_facecolor(bg_color)
ax1.set_facecolor(bg_color)

ax1.set_ylabel("Offences reported locally (Cambridgeshire)", fontsize=10, fontweight = 'bold', labelpad=20)
bar = ax1.bar(combined.index, local_crimes, color = colours[0], label="Local", width=0.5)
ax1.tick_params(axis='y')

ax2 = ax1.twinx()

ax2.set_ylabel("Offences reported nationally", fontsize=10, fontweight = 'bold', rotation=270, labelpad=20)
line = ax2.plot(combined.index, national_records, color = colours[2], label="National", linewidth=3, marker='o')
ax2.tick_params(axis='y')

ax1.set_title("Anti-social behaviour in Cambridgeshire vs Nationally", fontsize=15, fontweight='bold')

combined['Month'] = pd.to_datetime(combined['Month'])
x_labels = combined['Month'].dt.strftime('%b %Y') 
ax1.set_xticks(x, x_labels, rotation=30)
fig.legend(fontsize = 18)

fig.tight_layout()
plt.show()