import re
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from time import sleep, time
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.options import Options
from _datetime import datetime
import pandas as pd


def get_driver_info():
    chrome_options = Options()
    chrome_options.headless = True

    # webdriver.Chrome(ChromeDriverManager().install())

    driver = webdriver.Chrome(options=chrome_options,
                              executable_path='/Users/pushkarsingh/.wdm/drivers/chromedriver/mac64/99.0.4844.51'
                                              '/chromedriver')

    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver


def get_url_list(path):
    # Getting URLs list from csv file
    print(f"url file path is {path}")
    df = pd.read_csv(path, encoding='utf8')
    print(df)
    url_lists = df['URL'].tolist()
    url_lists = list(set(url_lists))
    for urls in url_lists:
        if urls == 'nan':
            url_lists.remove(urls)

    print(f"{url_lists}")
    return url_lists


def get_domain_name(url):
    filter_element = ['http://', 'https://', 'www.', '.com', '.net', '.us', '.uk',
                      'co.uk', '.io', '.org', '.co']
    for elements in filter_element:
        url = re.sub(elements, '', url)
        # print(f"Element & url are {elements} {url}")
    return url


def take_screenshot(url):
    driver = get_driver_info()
    driver.get(url)
    domain_name = get_domain_name(url)
    sleep(2)
    print(f"domain name is {domain_name}")
    current_datetime = datetime.now().strftime("%d_%m_%Y-%I:%M:%S_%p")
    current_datetime = current_datetime.replace(':', '-')

    file_name = f'{domain_name} screenshot at {current_datetime}.png'
    directory_path = "./data/screenshots/"
    full_file_path = directory_path + file_name
    driver.save_screenshot(full_file_path)
    print(f"Saved for {url}")
    driver.quit()


def prepare_screenshot(url_list=[]):
    threads = min(10, len(url_list))

    print(f"Threads are : {threads}")

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(take_screenshot, url_list)


def motor_function():
    # url_list = ['https://techgeekers.com', "https://ursuperb.com", 'https://www.forkandspoonkitchen.org',
    #             'http://veggievinder.com',]
    #
    url_list_path = './data/urls/urls_data.csv'
    url_list = get_url_list(url_list_path)

    prepare_screenshot(url_list)


if __name__ == '__main__':
    t0 = time()
    motor_function()
    t1 = time()
    print(f"{t1 - t0} seconds to perform")
