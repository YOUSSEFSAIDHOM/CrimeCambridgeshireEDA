
# Imports

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Fetching data
data = pd.read_csv('crimes.csv')
data = data.set_index('Crime Type')


# Population data from the ONS
cambridgeshire_population_pandemic = 678600
cambridgeshire_population_prepandemic = 621200
national_population_pandemic = 67080000
national_population_prepandemic = 66435550

# Storing data in variables from CSV file
local_pandemic = data['Local_Pandemic']
national_pandemic = data['National_Pandemic'] - local_pandemic # removing local from national
local_prepandemic = data['Local_Prepandemic']
national_prepandemic = data['National_Prepandemic'] - local_prepandemic

# Calculating rates per 1,000 of population

rate_local = np.divide(local_pandemic, cambridgeshire_population_pandemic*1000)
rate_national = np.divide(national_pandemic, (national_population_pandemic-cambridgeshire_population_pandemic)*1000)
rate_lpre = np.divide(local_prepandemic, cambridgeshire_population_prepandemic*1000)
rate_npre = np.divide(national_prepandemic, (national_population_prepandemic-cambridgeshire_population_prepandemic)*1000)

# Colour scheme 
colours = ["#1F271B", "#19647E", "#28AFB0", "#F4D35E", "#EE964B"]
bg_color = "#efe6dd"

# Plotting
fig, ax = plt.subplots()

fig.patch.set_facecolor(bg_color)
ax.set_facecolor(bg_color)

width = 0.25

x1 = np.arange(len(data.index))
x2 = [i + width for i in x1]

plt.barh(x2, rate_npre, width, color = colours[1], label="National pre-pandemic")
plt.barh(x1, rate_national, width, color = colours[0], label="National during-pandemic")
plt.barh(x2, -rate_lpre, width, color = colours[3], label='Local pre-pandemic')
plt.barh(x1,-rate_local, width, color = colours[4], label='Local during-pandemic')
plt.xlabel('Crime per 1,000 of population', fontsize=10, fontweight='bold')
plt.yticks(x1, data.index)
plt.yticks(rotation=30)
plt.legend(loc="upper right", fontsize=18)

ticks = ax.get_xticks()
ax.set_xticklabels([f'{abs(tick):.1e}' for tick in ticks])

ax.set_ylabel("Crimes Reported (Logged)", fontsize=10, fontweight = 'bold')
ax.set_title("Crimes per 1,000 of population, Cambridgeshire vs rest of the nation", fontsize=15, fontweight='bold')
plt.show()