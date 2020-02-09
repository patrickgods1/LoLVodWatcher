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
    # options = webdriver.ChromeOptions()
    # options.add_argument("--start-maximized")
    # options.add_argument('window-size=1920,1080')
    # browser = webdriver.Chrome(chrome_options=options)
    browser = webdriver.Chrome()

    browser.get('https://watch.lolesports.com/vods/')
    try:
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="riotbar-anonymous-link riotbar-account-action"]'))).click()
    except TimeoutException:
        print('[ERROR] Cannot find login button. Exiting.')
        return 0
    try:
        WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'html body.riotbar-present div main.Vods div.list div.VodsList')))
    except TimeoutException:
        print('[ERROR] Timed out waiting to be logged in. Exiting.')
        return 0
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.leagues > li.league > div.info')))
    except TimeoutException:
        print('[ERROR] VOD page did not load. Exiting.')
        return 0
    if not url:
        hrefs = []
        skip = ['https://watch.lolesports.com/vods/lcs-academy/na_academy_2020_split1']
        for league in browser.find_elements_by_css_selector('ul.leagues > li.league > div.info'):
            try:
                browser.execute_script("arguments[0].click();", league)
                WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.games > a.game')))
                if browser.current_url in skip:
                    print(f'[Skipped] {browser.current_url} is ineligible for watch rewards.')
                    continue
                hrefs = hrefs + [elm.get_attribute('href') for elm in browser.find_elements_by_css_selector(".game.watch-annotated:not(.watched)")]
            except TimeoutException:
                print(f'[ERROR] No links found on {browser.current_url}')
                continue
    else:
        hrefs = [elm.get_attribute('href') for elm in browser.find_elements_by_css_selector("div.games > a.game:not(.watched)")]
    print(f'[INFO] Found {len(hrefs)} links to watch.')
    tLower = t * 60 + 5
    tUpper = t * 60 + 88
    m = 0
    i = 0
    firstVid = True
    while i < len(hrefs):
        t = randint(tLower, tUpper)
        while m < multi and i < len(hrefs):
            browser.execute_script(f"window.open('{hrefs[i]}');")
            browser.switch_to_window(browser.window_handles[-1])
            try:
                WebDriverWait(browser, 1).until(EC.visibility_of_element_located((By.ID, 'video-player')))
            except TimeoutException:
                print(f'[ERROR] Timed out waiting for video player to load: {hrefs[i]}')
                browser.close()
                browser.switch_to.window(browser.window_handles[-1])
                i += 1
                continue
            browser.switch_to.frame('video-player-youtube')
            if firstVid:
                try:
                    # WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="ytp-large-play-button ytp-button"]'))).click()
                    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Play"]'))).click()
                except TimeoutException:
                    print(f'[ERROR] Timed out waiting to click play button. Continuing.')
                firstVid = False
                try:
                    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="ytp-mute-button ytp-button"]'))).click()
                except TimeoutException:
                    print(f'[ERROR] Timed out waiting for mute button. Continuing.')
            try:
                # WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="ytp-button ytp-settings-button"]'))).click()
                WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Settings"]'))).click()
                actions = ActionChains(browser)
                time.sleep(0.1)
                actions.send_keys(Keys.ARROW_DOWN * 5, Keys.ENTER, Keys.ARROW_DOWN * 6, Keys.ARROW_UP, Keys.ENTER)
                # 2x playback speed
                # actions.send_keys(Keys.ARROW_UP * 5, Keys.ENTER, Keys.ARROW_DOWN * 7, Keys.ENTER, Keys.ARROW_DOWN * 5, Keys.ENTER, Keys.ARROW_DOWN * 6, Keys.ARROW_UP, Keys.ENTER)
                actions.perform()
            except TimeoutException:
                print(f'[ERROR] Timed out waiting for settings button. Continuing.')
            try:
                browser.switch_to_default_content()
                WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'content')))
            except TimeoutException:
                print(f'[Skipped] {hrefs[i]} is ineligible for watch rewards.')
                browser.close()
                browser.switch_to.window(browser.window_handles[-1])
                i += 1
                continue
            print(f'[INFO] You are watching VOD number {i+1}: "{hrefs[i]}"')
            print(f'[INFO] Switching in {t} seconds')
            i += 1
            m += 1
        time.sleep(t)
        for _ in range(multi):
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
        m = 0

    browser.quit()
    print(f'[INFO] You have watched {len(hrefs)} VODs')


def main():
    while True:
        t = input(f'How long do you want to watch each VOD: (10 minutes minimum) ')
        if not t.isdigit():
            print(f'[ERROR] Response must be a number.')
            continue
        elif int(t) < 10:
            print(f'[ERROR] Response must be greater than 5 minutes.')
            continue
        else:
            break

    while True:
        multi = input(f'How many VODs do you want to watch simultaneously? ')
        if not multi.isdigit():
            print(f'[ERROR] Response must be a number.')
            continue
        elif int(multi) < 1:
            print(f'[ERROR] Response must greater than zero.')
            continue
        else:
            break

    url = input(f'URL to VODs page (Press ENTER to search through all links): ')
    if 'https://watch.lolesports.com/vods/' in url:
        watchVOD(url, int(t), int(multi))
    else:
        print(f"[INFO] No URL entered. Searching all leagues for links.")
        watchVOD(None, int(t), int(multi))


if __name__ == "__main__":
    main()
