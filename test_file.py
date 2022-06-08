import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def test_fullpage_screenshot():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("yoururlxxx")
    time.sleep(2)

    #the element with longest height on page
    ele=driver.find_element("xpath", '//div[@class="react-grid-layout layout"]')
    total_height = ele.size["height"]+1000

    driver.set_window_size(1920, total_height)      #the trick
    time.sleep(2)
    driver.save_screenshot("screenshot1.png")
    driver.quit()


if __name__ == "__main__":
    test_fullpage_screenshot()