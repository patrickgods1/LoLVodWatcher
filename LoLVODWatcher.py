from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import time
from random import randint


def watchVOD(url, t=600, multi=1):
    # url = "https://watch.na.lolesports.com/vods/cblol-brazil/cblol_2019_split1"
    # url = "https://watch.na.lolesports.com/vods/worlds/world_championship_2018"
    browser = webdriver.Chrome()

    browser.get(url)
    try:
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="riotbar-anonymous-link riotbar-account-action"]'))).click()
        # element = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "html body.riotbar-present div main.Vods div.list div.VodsList")))
        # browser.find_element_by_css_selector('a.riotbar-anonymous-link:nth-child(2)').click()
    except TimeoutException:
        print('Cannot find login button. Exiting.')
        return 0
    try:
        WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'html body.riotbar-present div main.Vods div.list div.VodsList')))
    except TimeoutException:
        print('Timed out waiting to be logged in. Exiting.')
        return 0

    hrefs = [elm.get_attribute('href') for elm in browser.find_elements_by_class_name('wrapper')]
    tLower = t * 60 + 5
    tUpper = t * 60 + 88
    m = 0
    i = 0
    while i < len(hrefs):
        t = randint(tLower, tUpper)
        while m < multi and i < len(hrefs):
            browser.execute_script(f"window.open('{hrefs[i]}');")
            # text = 'WATCH REWARDS ARE CORRECTLY SET UP FOR YOUR ACCOUNT'
            browser.switch_to_window(browser.window_handles[-1])
            try:
                WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.ID, 'video-player')))
            except TimeoutException:
                print('Timed out waiting for video player to load. Exiting.')
                return 0
            browser.switch_to.frame('video-player-youtube')
            if i == 0:
                try:
                    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="ytp-large-play-button ytp-button"]'))).click()
                except TimeoutException:
                    print(f'Timed out waiting for large play button. Continuing.')
                try:
                    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="ytp-mute-button ytp-button"]'))).click()
                except TimeoutException:
                    print(f'Timed out waiting for mute button. Continuing.')
            try:
                WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="ytp-button ytp-settings-button"]'))).click()
                actions = ActionChains(browser)
                time.sleep(0.3)
                # actions.send_keys(Keys.ARROW_DOWN * 5, Keys.ARROW_UP * 1, Keys.ENTER, Keys.ARROW_DOWN * 4, Keys.ENTER)
                actions.send_keys(Keys.ARROW_DOWN * 5, Keys.ENTER, Keys.ARROW_DOWN * 6, Keys.ARROW_UP, Keys.ENTER)
                actions.perform()
            except TimeoutException:
                    print(f'Timed out waiting for settings button. Continuing.')  
            
            print(f'You are watching VOD number: {i+1}')
            print(f'Switching in {t} seconds')
            i += 1
            m += 1
        time.sleep(t)
        for num in range(multi):
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
        m = 0

    browser.quit()
    print(f'You have watched {len(hrefs)} VODs')


def main():
    while True:
        t = input(f'How long do you want to watch each VOD: (10 minutes minimum) ')
        if not t.isdigit():
            print(f'Sorry, your response must be a number.')
            continue
        elif int(t) < 10:
            print(f'Sorry, your response must be greater than 10 minutes.')
            continue
        else:
            break

    while True:
        multi = input(f'How many VODs do you want to watch simultaneously? ')
        if not multi.isdigit():
            print(f'Sorry, your response must be a number.')
            continue
        elif int(multi) < 1:
            print(f'Sorry, your response must greater than zero.')
            continue
        else:
            break

    url = input(f'URL to VODs page: ')
    if 'https://watch.na.lolesports.com/vods/' in url:
        watchVOD(url, int(t), int(multi))
    else:
        print(f"Invalid URL. Defaulting to 'https://watch.na.lolesports.com/vods/cblol-brazil/cblol_2019_split1'")
        watchVOD(f'https://watch.na.lolesports.com/vods/cblol-brazil/cblol_2019_split1', int(t), int(multi))


if __name__ == "__main__":
    main()
