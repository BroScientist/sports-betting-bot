from bs4 import BeautifulSoup
from selenium import webdriver
import csv


def get_predictions_for_match(match_url):
    # match_url is whoscored.com preview link
    # this works but it's slow as shit (20+ seconds for one page...) but I don't wanna get banned again
    # it's slow because we are downloading the entire page... fuck this
    driver = webdriver.Chrome('/Users/apple/PycharmProjects/chromedriver')
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
        writer.writerow([team_names, scores])


# TODO write code to only find links for tmr's matches (or an arbitray range of days)
links = []
# for link in links:
#     get_predictions_for_match(link)

if __name__ == "__main__":
    get_predictions_for_match('https://www.whoscored.com/Matches/1376096/Preview/England-Premier-League-2019-2020-Crystal-Palace-Arsenal')