from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import datetime

links = []

driver = webdriver.Chrome('/Users/apple/PycharmProjects/chromedriver')
driver.get('https://www.whoscored.com/Previews')
page = driver.page_source
soup = BeautifulSoup(page, 'html.parser')
previews_date = soup.find('td', {'class': 'previews-date'}).text.strip()
tmr_date = str(datetime.date.today() + datetime.timedelta(days=1))

all_previews = soup.find('div', {'class': 'region previews'})
for link in all_previews.find_all('a', href=True):
    if 'Preview' in link['href']:
        links.append('https://www.whoscored.com/' + link['href'])


def get_predictions_for_match(driver, match_url):
    # match_url is whoscored.com preview link
    # this works but it's slow as shit (20+ seconds for one page...) but I don't wanna get banned again
    driver.get(match_url)
    page = driver.page_source

    soup = BeautifulSoup(page, 'html.parser')
    raw_scores = soup.find_all('span', {'class': 'predicted-score'})
    scores = [int(score.text) for score in raw_scores]
    raw_team_names = soup.find_all('a', {'class': 'team-link'})[:2]
    team_names = [name.text for name in raw_team_names]

    # convert teams and scores to string
    team_names = f'{team_names[0]} {team_names[1]}'
    scores = f'{scores[0]}-{scores[1]}'
    print(team_names)
    print(scores)

    with open('predictions.csv', 'a') as f:
        writer = csv.writer(f)
        team_names = team_names.replace('Manchester United', 'Manchester Utd')
        writer.writerow([team_names, scores])


with open('predictions.csv', 'w') as f:
    pass

num_of_bets = 10
for link in links[:num_of_bets]:
    try:
        get_predictions_for_match(driver, link)
    except:
        print('problem with webpage')

driver.quit()
