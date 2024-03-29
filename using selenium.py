from typing import List
import re
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from time import sleep, time
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import pandas as pd


def get_webdriver() -> webdriver.Chrome:
    """
    Returns a headless Chrome webdriver instance.
    """
    options = Options()
    options.headless = True
    return webdriver.Chrome(
        options=options,
        executable_path=ChromeDriverManager().install()
    )


def get_url_list(file_path: str) -> List[str]:
    """
    Parses a CSV file containing URLs and returns a list of unique URLs.
    """
    print(f"URL file path: {file_path}")
    df = pd.read_csv(file_path, encoding='utf8')
    urls = df['URL'].dropna().unique().tolist()
    print(f"URLs: {urls}")
    return urls


def get_domain_name(url: str) -> str:
    """
    Extracts the domain name from a given URL.
    """
    filter_elements = ['http://', 'https://', 'www.', '.com', '.net', '.us', '.uk',
                       'co.uk', '.io', '.org', '.co']
    for element in filter_elements:
        url = re.sub(element, '', url)
    return url


def take_screenshot(url: str) -> None:
    """
    Takes a screenshot of a webpage given its URL.
    """
    driver = get_webdriver()
    driver.get(url)
    domain_name = get_domain_name(url)
    sleep(2)
    current_datetime = datetime.now().strftime("%d_%m_%Y-%I:%M:%S_%p").replace(':', '-')
    file_name = f'{domain_name}_screenshot_{current_datetime}.png'
    directory_path = "./data/screenshots/"
    full_file_path = directory_path + file_name
    driver.save_screenshot(full_file_path)
    print(f"Saved screenshot for {url}")
    driver.quit()


def prepare_screenshots(url_list: List[str]) -> None:
    """
    Prepares and takes screenshots of multiple URLs concurrently.
    """
    threads = min(10, len(url_list))
    print(f"Number of threads: {threads}")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(take_screenshot, url_list)


def main() -> None:
    """
    Main function to execute the screenshot process.
    """
    url_list_path = './data/urls/urls_data.csv'
    url_list = get_url_list(url_list_path)
    prepare_screenshots(url_list)


if __name__ == '__main__':
    start_time = time()
    main()
    end_time = time()
    print(f"Execution time: {end_time - start_time} seconds")
