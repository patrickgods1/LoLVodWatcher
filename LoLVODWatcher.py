import configparser
import os
from random import randint
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

def printTime():
    print(f'[{time.strftime("%Y-%m-%d %I:%M:%S %p", time.localtime())}]', end='')


def watchVOD(userConfig):
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(chrome_options=options)
    browser.get('https://watch.lolesports.com/vods/')

    try:
        # WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'html body.riotbar-present div main.Vods div.list div.VodsList')))
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'html body.riotbar-present div main.Vods div.list div.VodsList')))
    except TimeoutException:
        printTime()
        print('[ERROR] VOD page did not load. Exiting.')
        return 0
    try:
        loginButton = browser.find_element_by_css_selector('#riotbar-account > div > a')
        menu = browser.find_element_by_css_selector('#riotbar-explore')   
        if loginButton.is_enabled() and loginButton.is_displayed():
            loginButton.click()
            # WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#riotbar-explore'))).click()
        elif menu.is_enabled() and menu.is_displayed():
            menu.click()
            # WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#riotbar-explore'))).click()
            WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#riotbar-navmenu-dropdown > div.riotbar-navmenu-category > a'))).click()
        else:
            # print(f'loginButton - is_enabled: {loginButton.is_enabled()} / is_displayed: {loginButton.is_displayed()}')
            # print(f'menu - is_enabled: {menu.is_enabled()} / is_displayed: {menu.is_displayed()}')         
            print('[ERROR] Cannot find login button. Exiting.')
            return 0
    except TimeoutException:
        printTime()
        print('[ERROR] Cannot find login button. Exiting.')
        return 0
    try:
        WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'html body.riotbar-present div main.Vods div.list div.VodsList')))
    except TimeoutException:
        printTime()
        print('[ERROR] Timed out waiting to be logged in. Exiting.')
        return 0
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.leagues > li.league > div.info')))
    except TimeoutException:
        printTime()
        print('[ERROR] VOD page did not load. Exiting.')
        return 0

    if not userConfig['Start URL']:
        hrefs = []
        skipRegionsList = [link.strip() for link in userConfig.get('Skip Regions List').split(',') if link]

        for league in browser.find_elements_by_css_selector('ul.leagues > li.league > div.info'):
            try:
                browser.execute_script("arguments[0].click();", league)
                WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.games > a.game')))
                if browser.current_url in skipRegionsList:
                    printTime()
                    print(f"[Skipped] {browser.current_url} is in Skip Regions List")
                    continue
                # hrefs = hrefs + [elm.get_attribute('href') for elm in browser.find_elements_by_css_selector("a.game.watch-annotated:not(.watched)")]
                hrefs = hrefs + [elm.get_attribute('href') for elm in browser.find_elements_by_xpath("//a[contains(@class, 'game') and not(contains(@class, 'watched'))]") if elm.get_attribute('href') not in userConfig['Skip Vods List']]
            except TimeoutException:
                printTime()
                print(f'[ERROR] No links found on {browser.current_url}')
                continue
    else:
        try:
            browser.get(userConfig['Start URL'])
            # WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.games > a.game')))
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.VodsList')))
        except TimeoutException:
            printTime()
            print('[ERROR] VOD page did not load. Exiting.')
        # hrefs = [elm.get_attribute('href') for elm in browser.find_elements_by_css_selector("div.games > a.game:not(.watched)")]
        hrefs = [elm.get_attribute('href') for elm in browser.find_elements_by_xpath("//a[contains(@class, 'game') and not(contains(@class, 'watched'))]") if elm.get_attribute('href') not in userConfig['Skip Vods List']]
    printTime()
    print(f'[INFO] Found {len(hrefs)} links to watch.')
    
    tLower = userConfig.getint('Time') * 60 + 5
    tUpper = userConfig.getint('Time') * 60 + 88
    m = 0
    i = 0
    firstVid = True
    watchCount = 0
    invalidList = []
    ineligibleList = []

    while i < len(hrefs):
        t = randint(tLower, tUpper)
        while m < userConfig.getint('Batch Size') and i < len(hrefs):
            browser.execute_script(f"window.open('{hrefs[i]}');")
            browser.switch_to_window(browser.window_handles[-1])
            try:
                WebDriverWait(browser, 1).until(EC.visibility_of_element_located((By.ID, 'video-player')))
            except TimeoutException:
                printTime()
                print(f'[ERROR] Timed out waiting for video player to load: {hrefs[i]}')
                invalidList.append(hrefs[i])
                browser.close()
                browser.switch_to.window(browser.window_handles[-1])
                i += 1
                continue
            browser.switch_to.frame('video-player-youtube')
            if firstVid:
                try:
                    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Play"]'))).click()
                except TimeoutException:
                    printTime()
                    print(f'[ERROR] Timed out waiting to click play button. Continuing.')
                firstVid = False
                try:
                    WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="ytp-mute-button ytp-button"]'))).click()
                except TimeoutException:
                    printTime()
                    print(f'[ERROR] Timed out waiting for mute button. Continuing.')
            try:
                WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Settings"]'))).click()
                actions = ActionChains(browser)
                time.sleep(0.1)
                actions.send_keys(Keys.ARROW_DOWN * 5, Keys.ENTER, Keys.ARROW_DOWN * 6, Keys.ARROW_UP, Keys.ENTER)
                # 2x playback speed
                # actions.send_keys(Keys.ARROW_UP * 5, Keys.ENTER, Keys.ARROW_DOWN * 7, Keys.ENTER, Keys.ARROW_DOWN * 5, Keys.ENTER, Keys.ARROW_DOWN * 6, Keys.ARROW_UP, Keys.ENTER)
                actions.perform()
            except TimeoutException:
                printTime()
                print(f'[ERROR] Timed out waiting for settings button. Continuing.')
            try:
                browser.switch_to_default_content()
                # WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'content')))
                WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.RewardsStatusInformer'))).click()
                rewardStatus = browser.find_element_by_css_selector('div.status > div.message')
                if rewardStatus.text.lower() == 'this game is not eligible for watch rewards':
                    printTime()
                    print(f'[Skipped] {hrefs[i]} is ineligible for watch rewards.')
                    ineligibleList.append(hrefs[i])
                    browser.close()
                    browser.switch_to.window(browser.window_handles[-1])
                    i += 1
                    continue
            except TimeoutException:
                printTime()
                print(f'[Skipped] {hrefs[i]} is ineligible for watch rewards.')
                ineligibleList.append(hrefs[i])
                browser.close()
                browser.switch_to.window(browser.window_handles[-1])
                i += 1
                continue
            printTime()
            print(f'[INFO] You are watching VOD number {watchCount+1}: "{hrefs[i]}"')
            printTime()
            print(f'[INFO] Watching for {t} seconds')
            i += 1
            m += 1
            watchCount += 1

        if m == 0:
            printTime()
            print(f'[ERROR] Ran out of videos to play.')
        else:
            time.sleep(t)
        for _ in range(m):
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])
        m = 0

    browser.quit()
    printTime()
    print(f'[INFO] You have watched {watchCount} VODs')
    if userConfig.getboolean('Output Ineligible Links'):
        if ineligibleList:
            printTime()
            print(f'[INFO] Outputting list of videos inelgible for rewards:')
            for l in ineligibleList:
                print(l)
        else:
            printTime()
            print(f'[INFO] Outputting list of videos inelgible for rewards: None found')

    if userConfig.getboolean('Output Invalid Links'):
        if invalidList:
            printTime()
            print(f'[INFO] Outputting list of links with no VODs found:')
            for l in invalidList:
                print(l)
        else:
            printTime()
            print(f'[INFO] Outputting list of links with no VODs found: None found')


def main():
    config = configparser.ConfigParser()
    try:
        with open('config.ini') as f:
            config.read(f)
    except IOError:
        print('[Info] Cannot find existing configuration file. Creating a new config.ini file.')
        config['DEFAULT'] = {'User Input Mode': 'true',
                                'Start URL': '',
                                'Batch Size': 2,
                                'Time': 15,
                                'Output Ineligible Links': 'false',
                                'Output Invalid Links': 'false',
                                'Skip Regions List': '',
                                'Skip VODs List': ''}
        config['User Configuration'] = {'User Input Mode': 'true',
                                'Start URL': '',
                                'Batch Size': 5,
                                'Time': 15,
                                'Output Ineligible Links': 'false',
                                'Output Invalid Links': 'false',
                                'Skip Regions List': '',
                                'Skip VODs List': ''}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    config.read('config.ini')
    userConfig = config['User Configuration']
    if userConfig.getboolean('User Input Mode'): # User input mode is on.
        while True:
            t = input(f'How long do you want to watch each VOD: (10 minutes minimum) ')
            if not t.isdigit():
                printTime()
                print(f'[ERROR] Response must be a number.')
                continue
            elif int(t) < 10:
                printTime()
                print(f'[ERROR] Response must be greater than 5 minutes.')
                continue
            else:
                break
        userConfig['Time'] = t

        while True:
            batchSize = input(f'How many VODs do you want to watch simultaneously? ')
            if not batchSize.isdigit():
                printTime()
                print(f'[ERROR] Response must be a number.')
                continue
            elif int(batchSize) < 1:
                printTime()
                print(f'[ERROR] Response must greater than zero.')
                continue
            else:
                break
        userConfig['Batch Size'] = batchSize

        url = input(f'URL to VODs page (Press ENTER to search through all links): ')
        if 'https://watch.lolesports.com/vods/' in url:
            userConfig['Start URL'] = url
        else:
            printTime()
            print(f"[INFO] No URL entered. Searching all leagues for links.")
        watchVOD(userConfig)

    else:   # User input is off. Use config.ini settings.
        printTime()
        print('[INFO] Using config.ini file settings.')
        watchVOD(userConfig)


if __name__ == "__main__":
    main()
