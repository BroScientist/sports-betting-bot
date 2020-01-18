from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import params
import csv

global initial_run_completed
initial_run_completed = False


def login(driver):

    url = 'https://sports.partypoker.com/en/sports'
    driver.get(url)
    # WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located)
    time.sleep(8)
    # locate and click the Login button
    # driver.find_element_by_css_selector("vn-menu-item[linkclass='header-btn btn']").click()
    driver.find_element_by_css_selector("vn-menu-item[linkclass='header-btn btn']").click()

    # locate and sendkeys to the username and passwords fields
    user_name_field = driver.find_element_by_css_selector("input[name='username']")
    user_name_field.click()
    user_name_field.send_keys(params.USERNAME)
    time.sleep(0.5)
    password_field = driver.find_element_by_css_selector("input[name='password']")
    password_field.send_keys(params.PASSWORD)
    password_field.send_keys(Keys.ENTER)

    # return True if my username shows up on the page after login
    time.sleep(5)
    return driver.find_element_by_css_selector("div[class='user-name']").text == params.USER_ID


def place_bet(driver, team_names, correct_score, stake):

    # locate the sports search button
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located)
    try:
        driver.find_element_by_css_selector("i[class='ui-icon ui-icon-size-lg sports-icon theme-search before-separator ng-star-inserted']").click()
    except:
        time.sleep(8)
        driver.find_element_by_css_selector("i[class='ui-icon ui-icon-size-lg sports-icon theme-search before-separator ng-star-inserted']").click()

    # locate the search bar and send keys
    search_bar = driver.find_element_by_css_selector("input[name='searchField']")
    search_bar.send_keys(team_names)
    search_bar.send_keys(Keys.ENTER)
    time.sleep(5)

    # locate the betting link in search results
    try:
        global initial_run_completed
        if not initial_run_completed:
            # bet_link = driver.find_element_by_css_selector("span[class='bet-builder-icon ng-star-inserted']")
            bet_link = driver.find_element_by_xpath('//*[@id="betfinder"]/div[3]/ms-grid/ms-event-group/ms-event/div/div/a/div[1]/ms-event-detail')
            initial_run_completed = True
        else:
            # bet_link = driver.find_element_by_css_selector("div[class='participant-container ng-star-inserted']")
            bet_link = driver.find_element_by_xpath('//*[@id="betfinder"]/div[3]/ms-grid/ms-event-group/ms-event/div/div/a/div[1]/ms-event-detail/ms-event-info')
        try:
            bet_link.click()
        except:
            driver.execute_script("arguments[0].click();", bet_link)
        # WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located) this doesn't work for some reason
        time.sleep(8)

        # locate the Correct Score betting page (it's simpler than scrolling down the page to find the Correct Score section)
        correct_score_box = driver.find_element_by_xpath("//*[text()='Correct score']")
        correct_score_box.click()
        score_box = driver.find_element_by_xpath(f".//div[text() = '{correct_score}']")
        score_box.click()

        # maximize the window because the bet box won't show up otherwise
        driver.maximize_window()

        # locate the input field, delete the default value of 5.00 and input the preset stake $$$ from params.py
        stake_input = driver.find_element_by_css_selector("input[tabindex='-1']")

        # stake_input.clear() doesn't work well with this site so we are using a for loop
        for _ in range(4):
            stake_input.send_keys(Keys.BACKSPACE)

        stake_input.send_keys(stake)

        # click the Place Bet button
        submit_btn = driver.find_element_by_css_selector("button[class='place betslip-place-button']")
        submit_btn.click()
        print(f'Bet: {team_names} {correct_score} (${stake}) has been placed')

    except Exception:
        print(f'Problem finding bets for: {team_names}')
        driver.get('https://sports.partypoker.com/en/sports')
        print('Navigating back to partypoker.com/en/sports')
        time.sleep(5)
        initial_run_completed = True
        raise Exception


driver = webdriver.Chrome('/Users/apple/PycharmProjects/chromedriver')

# continue to login until success (I know it's dumb as shit but this ain't the final product)
while not login(driver):
    login(driver)
print('Logged in successfully')

# place bet for every row in the predictions.csv file
with open('predictions.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        team_names = row[0]
        predicted_score = row[1]
        try:
            place_bet(driver, team_names, predicted_score, params.STAKE)
        except Exception:
            continue
driver.quit()
