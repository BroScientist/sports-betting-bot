from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import params

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
# search_bar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "i[class='ui-icon ui-icon-size-lg sports-icon theme-search before-separator ng-star-inserted']")))

time.sleep(10)
driver.find_element_by_css_selector("i[class='ui-icon ui-icon-size-lg sports-icon theme-search before-separator ng-star-inserted']").click()

# locate the search bar and send keys
search_bar = driver.find_element_by_css_selector("input[name='searchField']")
# search box can accept inputs for both teams ex. aston villa leicester city keys.Enter
search_bar.send_keys('Sheffield United West Ham')
search_bar.send_keys(Keys.ENTER)
time.sleep(2)
bet_link = driver.find_element_by_css_selector("ms-event[class='grid-event ms-active-highlight ng-star-inserted']")
bet_link.click()
time.sleep(5)

# locate the Correct Score betting page (it's simpler than scrolling down the page)
# TODO write code to accept input from file
correct_score_box = driver.find_element_by_xpath("//*[text()='Correct score']")
correct_score_box.click()
correct_score = '2-1'
score_box = driver.find_element_by_xpath(f".//div[text() = '{correct_score}']")
score_box.click()

# maximize the window because the bet box won't show up otherwise
driver.maximize_window()

# locate the input field, delete the default value of 5.00 and input the preset stake $$$ from params.py
stake_input = driver.find_element_by_css_selector("input[tabindex='-1']")
for _ in range(4):
    stake_input.send_keys(Keys.BACKSPACE)

stake_input.send_keys(params.STAKE)

# click the Place Bet button
submit_btn = driver.find_element_by_css_selector("button[class='place betslip-place-button']")
submit_btn.click()

# TODO write code to return to start and place new bet
'''
we can just click the search bar again and insert new input from csv

login and stuff
click search bar
for row in csv:
    place_bets(driver=driver, teams=row[0], correct_score=row[1])
    click search bar
finish
'''