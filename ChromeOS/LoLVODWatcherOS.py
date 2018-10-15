from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common import action_chains, keys # maybe for specific actions
import os
import time
from random import randint
import getpass


url = "https://watch.na.lolesports.com/vods/worlds/world_championship_2018"
loginURL = "https://auth.riotgames.com/authorize?client_id=rso-web-client-prod&redirect_uri=https%3A%2F%2Flogin.lolesports.com%2Foauth2-callback&scope=openid&response_type=code&state=lSbnyQxa5MHhB0beuFRuDz6cNgeoLCOJimJVDK3QRxM&ui_locales=en-us&login_hint=na"


PATH_TO_CHROME_DRIVER = '/Users/elisaur/Desktop/PythonScripts/LoLVODWatcher/ChromeOS/chromedriver'
driver = webdriver.Chrome(executable_path=PATH_TO_CHROME_DRIVER)

# Log in credentials
username = input("Username:")
password = getpass.getpass('Password:')
driver.get(loginURL)


WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="login-form-username"]')))  

driver.find_element_by_xpath('//*[@id="login-form-username"]').send_keys(username)
passfield = driver.find_element_by_xpath('//*[@id="login-form-password"]')
passfield.send_keys(password)

random_time = randint(1,3)
time.sleep(random_time)

# WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,'[//*[@id="login-button"]')))
# We can never find the above button anyways - riot is hiding it?

passfield.send_keys(u'\ue004') # That's press TAB when you're on the password field

actions = action_chains.ActionChains(driver)
actions.send_keys(keys.Keys.ENTER) # hit the Login button basically
actions.perform()

random_time = randint(1,3)
time.sleep(random_time)

driver.get(url)
WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "html body.riotbar-present div main.Vods div.list div.VodsList")))


try:
	driver.find_element_by_css_selector('a.riotbar-anonymous-link:nth-child(2)').click()
	element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "html body.riotbar-present div main.Vods div.list div.VodsList")))
except NoSuchElementException:
	print('Cannot find login button')

hrefs = (elm.get_attribute('href') for elm in driver.find_elements_by_css_selector("div.VodsList > a"))



for i, link in enumerate(hrefs):
	driver.get(link)
	print(f"You're watching VOD number: {i+1}")
	t = randint(615, 678)
	print(f"Switching in {t} seconds")
	time.sleep(t)

driver.quit()
print(f"You've watched {len(hrefs)} VODs")