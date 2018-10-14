from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import configparser
import os
import time
from random import randint

url = "https://watch.na.lolesports.com/vods/worlds/world_championship_2018"
loginURL = "https://auth.riotgames.com/authorize?client_id=rso-web-client-prod&redirect_uri=https%3A%2F%2Flogin.lolesports.com%2Foauth2-callback&scope=openid&response_type=code&state=lSbnyQxa5MHhB0beuFRuDz6cNgeoLCOJimJVDK3QRxM&ui_locales=en-us&login_hint=na"
mozilla_profile = os.path.join(os.getenv('APPDATA'), r'Mozilla\Firefox')
mozilla_profile_ini = os.path.join(mozilla_profile, r'profiles.ini')
profile = configparser.ConfigParser()
profile.read(mozilla_profile_ini)
data_path = os.path.normpath(os.path.join(mozilla_profile, profile.get('Profile0', 'Path')))
# print(data_path)
fp = webdriver.FirefoxProfile(data_path)
browser = webdriver.Firefox(fp)

browser.get(url)
element = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "html body.riotbar-present div main.Vods div.list div.VodsList")))
try:
	browser.find_element_by_css_selector('a.riotbar-anonymous-link:nth-child(2)').click()
	element = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "html body.riotbar-present div main.Vods div.list div.VodsList")))
except NoSuchElementException:
	print('Cannot find login button')

hrefs = [elm.get_attribute('href') for elm in browser.find_elements_by_css_selector("div.VodsList > a")]
print(len(hrefs))

for href in hrefs:
	browser.get(href)
	time.sleep(randint(615, 678))

browser.quit()
print(f"You've watched {len(hrefs)} VODs")