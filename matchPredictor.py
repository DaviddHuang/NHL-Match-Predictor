import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

url = 'https://www.hockey-reference.com/leagues/NHL_2024_standings.html'
matches = []
data = requests.get(url)
soup = BeautifulSoup(data.content, 'html.parser')
teams_table = soup.select('table.stats_table')[0]
links = teams_table.findAll('a')
teams_table2 = soup.select('table.sortable')[1]
links2 = teams_table2.findAll('a')
combined_links = links + links2
combined_links = [l.get('href') for l in combined_links]
combined_links = [l for l in combined_links if '/teams/' in l]
teams = [f"https://www.hockey-reference.com{l.replace('.html', '_gamelog.html')}" for l in combined_links]

for team_url in teams:
    team_data = requests.get(team_url)
    games = pd.read_html(team_data.text, match="Regular Season")[0]
    games.columns = [
        'GP', 'Date', 'Venue', 'Opponent', 'GF', 'GA', 'Result', 
        'OT Result', 'Unnamed: 8_level_1', 'S', 'PIM', 'PPG', 'PPO', 'SHG','Unnamed: 14_level_1',
        'OS', 'OPIM', 'OPPG', 'OPPO', 'OSHG','Unnamed: 15_level_1', 'CF', 'CA', 'CF%', 'FF', 'FA', 
        'FF%', 'FOW', 'FOL', 'FO%', 'oZS%', 'PDO'
    ]
    games = games[~games['GP'].astype(str).str.contains('GP')]
    matches.append(games)
    time.sleep(5)

stat_df = pd.concat(matches)
stat_df = stat_df.drop(columns=['Unnamed: 8_level_1', 'OS', 'OPIM', 'OPPG', 'OPPO', 'OSHG', 'Unnamed: 14_level_1', 'Unnamed: 15_level_1'])
stat_df['Venue'] = stat_df['Venue'].replace('@', 'Away')
stat_df['Venue'] = stat_df['Venue'].fillna('Home').replace('', 'Home')
stat_df.to_csv("matches.csv", index=False)



