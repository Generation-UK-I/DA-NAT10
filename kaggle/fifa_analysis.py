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