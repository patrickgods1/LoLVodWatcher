from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains
import configparser
import os
import time
from random import randint

def watchVOD(t=600, multi=1):
	url = "https://watch.na.lolesports.com/vods/worlds/world_championship_2018"
	# mozilla_profile = os.path.join(os.getenv('APPDATA'), r'Mozilla\Firefox')
	# mozilla_profile_ini = os.path.join(mozilla_profile, r'profiles.ini')
	# profile = configparser.ConfigParser()
	# profile.read(mozilla_profile_ini)
	# data_path = os.path.normpath(os.path.join(mozilla_profile, profile.get('Profile0', 'Path')))
	# # print(data_path)
	# fp = webdriver.FirefoxProfile(data_path)
	# browser = webdriver.Firefox(fp)

	browser = webdriver.Chrome()

	browser.get(url)
	element = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "html body.riotbar-present div main.Vods div.list div.VodsList")))
	try:
	  browser.find_element_by_css_selector('a.riotbar-anonymous-link:nth-child(2)').click()
	  element = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "html body.riotbar-present div main.Vods div.list div.VodsList")))
	except NoSuchElementException:
	  print('Cannot find login button')

	hrefs = [elm.get_attribute('href') for elm in browser.find_elements_by_css_selector("div.VodsList > a")]
	#print(len(hrefs))
	tLower = t*60 + 5
	tUpper = t*60 + 99
	m = 0
	i = 0
	#for i in range(0,len(hrefs)):
	#while i < len(hrefs) and m < multi:
	while i < len(hrefs):
		t = randint(tLower, tUpper)
		while m < multi and i < len(hrefs):
			browser.execute_script(f"window.open('{hrefs[i]}');")
			#time.sleep(5)
			text = 'WATCH REWARDS ARE CORRECTLY SET UP FOR YOUR ACCOUNT'
			# WATCH REWARDS ARE CORRECTLY SET UP FOR YOUR ACCOUNT
			#element = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, content")]')))
			#elem = browser.find_element_by_xpath('//*[contains(@class, "content")]')
			if i == 0:
				print("Mute and change resolution to 144p")
				time.sleep(5)
			browser.switch_to_window(browser.window_handles[-1])
			element = WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.XPATH, '//*[contains(@class, "content")]')))
			#browser.get(hrefs[i])
			print(f"You're watching VOD number: {i+1}")
			print(f"Switching in {t} seconds")
			i += 1
			m += 1
		time.sleep(t)
		for num in range(multi):
			browser.close()
			browser.switch_to.window(browser.window_handles[-1])
		#browser.switch_to.window(browser.window_handles[0])
		m = 0

	browser.quit()
	print(f"You've watched {len(hrefs)} VODs")

def main():
	while True:
		t = input("How long do you want to watch each VOD: (10 minutes minimum) ")
		if not t.isdigit():
			print("Sorry, your response must be a number.")
			continue
		elif int(t) < 10:
			print("Sorry, your response must be greater than 10 minutes.")
			continue
		else:
			break

	while True:
		multi = input("How many VODs do you want to watch simultaneously? ")
		if not multi.isdigit():
			print("Sorry, your response must be a number.")
			continue
		elif int(multi) < 1:
			print("Sorry, your response must greater than zero.")
			continue
		else:
			break

	watchVOD(int(t), int(multi))

if __name__ == "__main__":
	main()
