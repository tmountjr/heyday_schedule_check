"""Scan the team schedule page and note any differences from the previous scan.
"""

import re
import requests
from bs4 import BeautifulSoup

URL = 'https://delaware.leaguelab.com/team/675631'
page = requests.get(URL, timeout=5)

soup = BeautifulSoup(page.content, 'html.parser')
team_schedule_table = soup.find(id='teamScheduleTable')

# Find all tr elements with an id that matches the regex /^game_\d+_\d+$/
game_rows = team_schedule_table.find_all('tr', id=re.compile(r'^game_\d+_\d+$'))

# Within each game_row, there is one td with an id that matches the regex
# /^game_YYYY-MM-DD_HH-MM AM/.
# Capture the date and time from the td's id.
game_dates = []
id_regex = re.compile(r'^game_([\d\-]+_[\d\-]+) .*')
for game_row in game_rows:
    game_td = game_row.find('td', id=id_regex)
    if game_td is not None:
        game_id = game_td.get('id')
        results = re.search(id_regex, game_id)
        game_date = results.group(1)
        game_dates.append(game_date)

game_dates.sort()

with open('previous.txt', 'r', encoding='utf-8') as f:
    previous_games = [line.rstrip() for line in f]

previous_games.sort()
if game_dates == previous_games:
    print('No schedule changes found.')
else:
    print('Schedule changes found:')
    with open('previous.txt', 'w', encoding='utf-8') as f:
        for game_date in game_dates:
            if game_date not in previous_games:
                print(f'New game date/time: {game_date}')
            f.write(game_date + '\n')
