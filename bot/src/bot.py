from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
from config import Config

PROFILE = Config.PROFILE_PATH
CHROMIUM = Config.CHROMIUM_PATH

def createBrowserInstance(website, headfull=False, wait_time_instance=150):
    service = Service(CHROMIUM)
    options = webdriver.ChromeOptions()

    # Set user agent to a valid Chrome user agent
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    options.add_argument(f'--user-agent={user_agent}')

    # Set a valid window size for headless mode
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--window-position=0,0')

    # Add the following options to mimic a normal browser
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    # Exclude automation switches
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Set language and disable automation features
    options.add_argument('--lang=en-US')
    options.add_argument('--disable-blink-features=AutomationControlled')

    if not headfull and os.path.isdir(PROFILE): # Set the user data directory,
        # if it already exists we can run in headless mode otherwise need to link
        options.add_argument('--headless=new')

    options.add_argument(f"--user-data-dir={PROFILE}")

    driver = webdriver.Chrome(service=service, options=options)

    # Modify navigator.webdriver and other properties that indicate automation, such as navigator.webdriver:
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'mimeTypes', { get: () => [1, 2, 3, 4, 5] });
        '''
    })

    driver.get(website)
    time.sleep(wait_time_instance)
    return driver

def sendMessage(driver, contact, message, wait_time_send=30):
    time.sleep(wait_time_send)
    search_box = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p')
    search_box.click()
    search_box.send_keys(contact)

    # Wait for the contactname to appear in the search results
    time.sleep(wait_time_send)

    # Select the contactname
    contactname = driver.find_element(By.XPATH, f"//div[.//span[contains(@title, '{contact}')]]/ancestor::div[@role='gridcell']")
    contactname.click()
    # Wait for the chat to load
    time.sleep(wait_time_send)

    # Find the message box and enter the message
    message_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]')
    message_box.click()
    message_box.send_keys(message)

    time.sleep(wait_time_send)
    # Find the send button and click it
    send_button = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[2]/button/span')
    send_button.click()
    time.sleep(wait_time_send)

def selectContact(driver, contact, wait_time_select=30):
    time.sleep(wait_time_select)
    search_box = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p')
    search_box.click()
    search_box.send_keys(contact)

    # Wait for the contactname to appear in the search results
    time.sleep(wait_time_select)

    # Select the contactname
    contactname = driver.find_element(By.XPATH, f"//div[.//span[contains(@title, '{contact}')]]/ancestor::div[@role='gridcell']")
    contactname.click()

    time.sleep(wait_time_select)
    for i in range(len(contact)):
        search_box.send_keys(Keys.BACK_SPACE)


if __name__ == '__main__':
    import helpers
    from datetime import datetime

    CONFIG_API_URL = Config.CONFIG_API_URL

    TODAY = datetime.today()

    test_logger = helpers.setup_logger('test_logger')

    driver_og = createBrowserInstance(website='https://web.whatsapp.com', headfull=True)
    test_logger.info('Opened the browser')

    name = "Nützlichs!"
    work = "be happy"
    text = f"Dringende Mitteilung, sie müssen diese Woche: --> *{work}* <--"

    sendMessage(driver=driver_og, contact=name, message=text)
    test_logger.info(f'{name} received the message')