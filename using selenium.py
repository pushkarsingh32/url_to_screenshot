from typing import List
import re
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from time import sleep, time
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import pandas as pd
import os
from urllib.parse import urlparse


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

    # Create directory if it doesn't exist
    directory_path = os.path.dirname(file_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
    # Create CSV file if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            pass

    # Check if CSV file is empty
    if os.stat(file_path).st_size == 0:
        raise ValueError("CSV file is empty")

    df = pd.read_csv(file_path, encoding='utf8')

    # Check if 'URL' column exists in the CSV file
    if 'URL' not in df.columns:
        raise ValueError("CSV file doesn't contain 'URL' column")

    # Validate URLs format
    urls = df['URL'].dropna().unique().tolist()
    for url in urls:
        if not re.match(r'^https?://', url):
            raise ValueError(f"Invalid URL format: {url}")

    print(f"URLs: {urls}")
    return urls


# def get_domain_name(url: str) -> str:
#     """
#     Extracts the domain name from a given URL.
#     """
#     filter_elements = ['http://', 'https://', 'www.', '.com', '.net', '.us', '.uk',
#                        'co.uk', '.io', '.org', '.co']
#     for element in filter_elements:
#         url = re.sub(element, '', url)
#     return url
def get_domain_name(url: str, include_subdomains: bool = False) -> str:
    """
    Extracts the domain name from a given URL.
    """
    try:
        parsed_url = urlparse(url)
        if include_subdomains:
            domain = parsed_url.netloc
        else:
            domain_parts = parsed_url.netloc.split('.')
            if len(domain_parts) >= 2:
                domain = '.'.join(domain_parts[-2:])
            else:
                domain = parsed_url.netloc
        # Normalize domain name to lowercase
        domain = domain.lower()
        return domain
    except Exception as e:
        print(f"Error extracting domain name: {e}")
        return ""
    

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
    
    # Create directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        
    full_file_path = os.path.join(directory_path, file_name)
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
    # Save your url list file in csv format in below location
    url_list_path = './data/urls/urls_data.csv'
    
    try:
        url_list = get_url_list(url_list_path)
        if not url_list:
            raise NoURLsFoundError("No URLs found in the URL list file.")
        prepare_screenshots(url_list)
    except FileNotFoundError:
        print(f"Error: CSV file '{url_list_path}' not found")
    except ValueError as ve:
        print(f"Error: {ve}")


if __name__ == '__main__':
    start_time = time()
    main()
    end_time = time()
    print(f"Execution time: {end_time - start_time} seconds")
