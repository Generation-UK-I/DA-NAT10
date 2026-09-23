# FIFA 2026

## Relational Exploratory Data

### Code

```py
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. DYNAMIC PATH CHECKER (Works on Kaggle AND Local Machine)
input_dir = '/kaggle/input' if os.path.exists('/kaggle/input') else '.'

csv_files = {}
for dirname, _, filenames in os.walk(input_dir):
    for filename in filenames:
        if filename.endswith('.csv'):
            name = filename.replace('.csv', '')
            csv_files[name] = os.path.join(dirname, filename)

print("Found Dataset Files:")
for name, path in csv_files.items():
    print(f" - {name}: {path}")

# Check if files were actually found
if not csv_files:
    raise FileNotFoundError("No CSV files found. Please make sure the CSV files are in the same folder as this script.")

# 2. ENCODING FIX (Specifying utf-8 for Windows compatibility)
teams = pd.read_csv(csv_files['teams'], encoding='utf-8')
players = pd.read_csv(csv_files['squads_and_players'], encoding='utf-8')
venues = pd.read_csv(csv_files['venues'], encoding='utf-8')
matches = pd.read_csv(csv_files['matches_detailed'], encoding='utf-8')
events = pd.read_csv(csv_files['match_events'], encoding='utf-8')

print(f"\nData Loaded Successfully! Player count: {len(players)}, Match count: {len(matches)}")

# Plotting Settings
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Graph 1: Stadium Capacities
plt.figure()
sns.barplot(data=venues.sort_values(by='capacity', ascending=False), 
            x='capacity', y='stadium_name', hue='country', palette='viridis')
plt.title('FIFA World Cup 2026 - Stadium Capacities by Country', fontsize=16, fontweight='bold')
plt.xlabel('Seating Capacity')
plt.ylabel('Stadium Name')
plt.tight_layout()
plt.show()

# Graph 2: Elo vs Market Value
team_values = players.groupby('team_id')['market_value_eur'].sum().reset_index()
team_stats = pd.merge(teams, team_values, on='team_id')

plt.figure(figsize=(10, 6))
sns.scatterplot(data=team_stats, x='elo_rating', y='market_value_eur', 
                size='fifa_ranking_pre_tournament', hue='confederation', 
                sizes=(40, 400), alpha=0.7, palette='Set2')
plt.title('Team Elo Rating vs Total Player Market Value', fontsize=16, fontweight='bold')
plt.xlabel('Elo Rating')
plt.ylabel('Total Squad Market Value (EUR)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Graph 3: Top Clubs represented (Seaborn Palette fix applied)
top_clubs = players['club_team'].value_counts().head(10).reset_index()
top_clubs.columns = ['Club', 'Player Count']

plt.figure()
sns.barplot(data=top_clubs, x='Player Count', y='Club', hue='Club', legend=False, palette='rocket')
plt.title('Top 10 Club Teams Represented in FIFA World Cup 2026', fontsize=16, fontweight='bold')
plt.xlabel('Number of Registered Players')
plt.ylabel('Club Team')
plt.tight_layout()
plt.show()

# Graph 4: Heights and Goals by Position (Seaborn Palette fix applied)
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.histplot(data=players, x='height_cm', hue='position', multiple='stack', 
             kde=True, ax=axes[0], palette='crest')
axes[0].set_title('Distribution of Player Heights by Position', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Height (cm)')

sns.boxplot(data=players[players['goals'] > 0], x='position', y='goals', 
            hue='position', legend=False, ax=axes[1], palette='pastel')
axes[1].set_title('International Goals by Position (Players with > 0 goals)', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Position')
axes[1].set_ylabel('International Goals')

plt.tight_layout()
plt.show()
```

### Breakdown

>If you wish to run the analysis locally you can download them from here: [FIFA World Cup 2026 Dataset](https://www.kaggle.com/datasets/mominullptr/fifa-world-cup-2026-dataset)

```py
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```

Import required libraries

```py
input_dir = '/kaggle/input' if os.path.exists('/kaggle/input') else '.'
```

Looks for input files in `/kaggle/input` or in the current working directory `.` ensuring that it can run locally as well as in **Kaggle**.

```py
csv_files = {}
for dirname, _, filenames in os.walk(input_dir):
    for filename in filenames:
        if filename.endswith('.csv'):
            name = filename.replace('.csv', '')
            csv_files[name] = os.path.join(dirname, filename)
```

Create an empty dictionary `csv_files = {}` then loop through the folders and subfolders `os.walk(input_dir)` to find the files within.

>`os.walk()` returns a 3-tuple, containing directory, subdirectory, and filenames. For the purpose of this script we don't need the subdirectory, so rather than declaring a variable, e.g. **subdirname**, that is unused, by convention we use an underscore to indicate that there is a value, but we don't need it.

Loop through the `input_dir` and for each file that is found, if it ends with `'.csv'`, then replace it with `''` (an empty string), basically stripping off the extension, so `teams.csv` becomes `teams` and that is assigned to the `name` variable.

Finally each `name`is added to the `csv_files` dictionary as a key, along with the original dirname and filename as the value, creating entries such as: `"teams":"input/teams.csv"`.

```py
print("Found Dataset Files:")
for name, path in csv_files.items():
    print(f" - {name}: {path}")
...
if not csv_files:
    raise FileNotFoundError("...")
```

Print out the discovered files, or raise an error if no csv's are found.

```py
teams = ...
players = ...
venues = ...
matches = ...
events = pd.read_csv(csv_files['match_events'], encoding='utf-8')
```

Each of the required files is loaded into a Pandas DataFrame by calling the file path from it's corresponding key. `encoding='utf-8'` ensures that special characters are rendered correctly.

```py
print(f"\nData Loaded Successfully! Player count: {len(players)}, Match count: {len(matches)}")
```

Prints the number of players and matches, given one per line in the corresponding csv files.

```py
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
```

Sets the default style for Seaborn (white background and gridlines), and size of our desired plot (12x6 inches).

```py
plt.figure()
sns.barplot(data=venues.sort_values(by='capacity', ascending=False), 
            x='capacity', y='stadium_name', hue='country', palette='viridis')
plt.title('FIFA World Cup 2026 - Stadium Capacities by Country', fontsize=16, fontweight='bold')
plt.xlabel('Seating Capacity')
plt.ylabel('Stadium Name')
plt.tight_layout()
plt.show()
```

Generate the first plot ranking stadium sizes:

- Use a Seaborn barplot
- Sort data in the venues csv by capacity, ascending.
- Define the `x` and `y` axes
- Use the viridis colour palette, and base the hue on the different countries
- Provide a title, font size, and weight
- Label the axis and select the tight layout
- Display the plot

Generate the next plot comparing ELO (a mathematical skill ranking) to the value of the team

```py
team_values = players.groupby('team_id')['market_value_eur'].sum().reset_index()
team_stats = pd.merge(teams, team_values, on='team_id')

plt.figure(figsize=(10, 6))
sns.scatterplot(data=team_stats, x='elo_rating', y='market_value_eur', 
                size='fifa_ranking_pre_tournament', hue='confederation', 
                sizes=(40, 400), alpha=0.7, palette='Set2')
plt.title('Team Elo Rating vs Total Player Market Value', fontsize=16, fontweight='bold')
plt.xlabel('Elo Rating')
plt.ylabel('Total Squad Market Value (EUR)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
```

- `team_values = players.groupby('team_id')['market_value_eur'].sum().reset_index()`: Groups the players DataFrame, loaded earlier, by `team_id`, then selects the `'market_value_eur'` column within each group, and sums these values. `.reset_index()` resets the current index: `team_id` to a regular column, producing a clean DataFrame. The resulting frame is assigned to `team_values`.
- `team_stats = pd.merge(teams, team_values, on='team_id')`: Creates a new DataFrame by merging the new `team_values` frame with the existing `teams` frame, which contains the ELO rating we require. The frames are merged on the `team_id` field.
- `plt.figure(figsize=(10, 6))`: Define the size of the plot
- `sns.scatterplot...`: Many of the characteristics are similar to the previous plot with a few additions for a bubble chart (a type of scatter plot in which the bubble size represents a third variable).
  - `size='fifa_ranking_pre_tournament'`: The third variable
  - `sizes=(40, 400)`: The lower and upper sizes of the bubbles - NOTE: the top ranked team is the smallest bubble, bottom ranked is the largest.
  - `alpha=0.7`: Bubble transparency

```py
plt.title...
plt.xlabel...
plt.ylabel...
plt.legend...
plt.tight_layout()
plt.show()
```

- Define titles, labels, axes, and layout.
- Add a legend and display the plot

You should be able to decipher plots 3 and 4 based on what we've covered so far.