from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import params
import csv

driver = webdriver.Chrome('/Users/apple/PycharmProjects/chromedriver')
url = 'https://sports.partypoker.com/en/sports'
driver.get(url)
# page = driver.page_source

# login to Partypoker.com
time.sleep(3)
driver.find_element_by_css_selector("vn-menu-item[linkclass='header-btn btn']").click()
user_name_field = driver.find_element_by_css_selector("input[name='username']")
user_name_field.click()
user_name_field.send_keys(params.USERNAME)
password_field = driver.find_element_by_css_selector("input[name='password']")
password_field.send_keys(params.PASSWORD)
password_field.send_keys(Keys.ENTER)

# locate the sports search button

# wait = WebDriverWait(driver, 15)
# sports_search = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "i[class='ui-icon ui-icon-size-lg sports-icon theme-search before-separator ng-star-inserted']")))
# sports_search.click()


global initial_run_completed
initial_run_completed = False


def place_bet(driver, team_names, correct_score):
    time.sleep(5)
    driver.find_element_by_css_selector("i[class='ui-icon ui-icon-size-lg sports-icon theme-search before-separator ng-star-inserted']").click()

    # locate the search bar and send keys
    search_bar = driver.find_element_by_css_selector("input[name='searchField']")
    # search box can accept inputs for both teams ex. aston villa leicester city keys.Enter
    search_bar.send_keys(team_names)
    search_bar.send_keys(Keys.ENTER)
    time.sleep(4)
    try:
        global initial_run_completed
        if not initial_run_completed:
            bet_link = driver.find_element_by_css_selector("span[class='bet-builder-icon ng-star-inserted']")
            initial_run_completed = True
        else:
            bet_link = driver.find_element_by_css_selector("div[class='participant-container ng-star-inserted']")
        try:
            bet_link.click()
        except:
            driver.execute_script("arguments[0].click();", bet_link)
        time.sleep(7)
        # locate the Correct Score betting page (it's simpler than scrolling down the page)
        # TODO write code to accept input from file
        correct_score_box = driver.find_element_by_xpath("//*[text()='Correct score']")
        correct_score_box.click()
        score_box = driver.find_element_by_xpath(f".//div[text() = '{correct_score}']")
        score_box.click()

        # maximize the window because the bet box won't show up otherwise
        driver.maximize_window()

        # locate the input field, delete the default value of 5.00 and input the preset stake $$$ from params.py
        stake_input = driver.find_element_by_css_selector("input[tabindex='-1']")
        # stake_input.clear()
        for _ in range(4):
            stake_input.send_keys(Keys.BACKSPACE)

        stake_input.send_keys(params.STAKE)

        # click the Place Bet button
        submit_btn = driver.find_element_by_css_selector("button[class='place betslip-place-button']")
        submit_btn.click()
    except Exception:
        print(Exception)
        print('no results found')
        driver.get('https://sports.partypoker.com/en/sports')
        time.sleep(4)
    finally:
        print('bet successfully processed')


with open('predictions.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        team_names = row[0]
        predicted_score  = row[1]
        place_bet(driver, team_names, predicted_score)
    driver.quit()