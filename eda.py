from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import numpy as np

def get_quarter_scores(url):
    html = urlopen(f'https://www.pro-football-reference.com/{url}')
    # print(url)
    soup = BeautifulSoup(html)
    scores = soup.find('div', class_='linescore_wrap').find('table').find('tbody')
    team_qtr_scores = []
    for scoreline in scores.findAll('tr'):
        team_qtr_scores.append([int(value.getText()) for value in scoreline.findAll('td')[2:-1]])
    tups = []     
    for i in range(len(team_qtr_scores[0])):
        tups.append((sum(team_qtr_scores[0][:i+1]) % 10, sum(team_qtr_scores[1][:i+1]) % 10))
    return tups


url = "https://www.pro-football-reference.com/years/2023/games.htm"
html = urlopen(url)
soup = BeautifulSoup(html)
games = soup.find('table', id='games')
flag = False
scores = []
for row in games.findAll('tr'):
    time.sleep(3)
    for value in row.findAll('td'):
        if value.getText() == 'boxscore':
            boxscore_url = value.find('a').attrs['href']
            tups = get_quarter_scores(boxscore_url)
            scores.extend(tups)

arr = np.zeroes(shape=(10,10))
for score in scores:
    arr[score[0]-1, score[1]-1] += 1
print(arr)

