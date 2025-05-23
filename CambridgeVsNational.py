import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

national = pd.read_csv('National_Crime_Recs_PM_(ALL_TYPES).csv')
local = pd.read_csv('Crime_Cambridgeshire.csv')


combined = national.merge(local, left_on='Month', right_on='Month')
combined_months = combined.set_index('Month')

normalised_combined = (combined_months - combined_months.mean())/combined_months.std()
x = normalised_combined.index
national_records = normalised_combined['Records']
local_crimes = normalised_combined['Crimes']

national_log = np.log10(national_records)
local_log = np.log10(local_crimes)

combined['Month'] = pd.to_datetime(combined['Month'])
x_labels = combined['Month'].dt.strftime('%b %Y') 

colours = ["#1F271B", "#19647E", "#28AFB0", "#F4D35E", "#EE964B"]
bg_color = "#efe6dd"

width = 0.25
fig, ax = plt.subplots()

fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)
x1 = np.arange(len(x))
x2 = [i + width for i in x1]
plt.bar(x1, national_records, width, color = colours[0], label="National Crimes")
plt.bar(x2, local_crimes, width, color = colours[1], label='Local Crimes')
# plt.plot(x1, national_records, color=colours[0], label='National Records', marker='o')
# plt.plot(x1, local_crimes, color=colours[1], label='Local Crimes', marker='o')
plt.xlabel('Date', fontsize=10, fontweight='bold')
plt.xticks(x1, x_labels)
plt.xticks(rotation=30)
plt.legend(loc="upper right", fontsize=18)
plt.axhline(y=0, color='black')
ax.set_ylabel("Crimes Reported (Normalised)", fontsize=10, fontweight = 'bold')
ax.set_title("Local vs National Crime Statistics", fontsize=15, fontweight='bold')
plt.show()