# URL to Screenshot (Webpage Screenshot Tool)

## Overview
This is a Python script that captures screenshots of web pages listed in a CSV file concurrently using Selenium WebDriver. It is designed to efficiently handle a large number of URLs and capture screenshots in parallel, making it suitable for tasks like website monitoring, testing, or generating previews.

## Features
- **Concurrent Execution**: Utilizes Python's ThreadPoolExecutor for concurrent execution of screenshot capture tasks, enhancing performance.
- **Flexible Configuration**: Easily configurable via the provided CSV file containing URLs to capture screenshots of.
- **Headless Mode**: Supports headless execution, allowing it to run in the background without launching a browser window.
- **Customizable Naming**: Screenshots are named based on the domain name and timestamp, ensuring uniqueness and easy identification.

## Requirements
- Python 3.x
- Chrome WebDriver
- Selenium
- Pandas
- Webdriver Manager

## Installation
1. Clone the repository:

    ```bash
    git clone https://github.com/pushkarsingh32/webpage-screenshot-tool.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Make sure to have Chrome WebDriver installed. If not, it can be automatically installed using the Webdriver Manager.

## Usage
1. Prepare a CSV file containing a list of URLs under a column named "URL". Ensure there are no duplicate or empty URLs.

2. Run the script by executing the following command:

    ```bash
    python screenshot_tool.py
    ```

3. Screenshots will be saved in the specified directory (`./data/screenshots/`) with filenames in the format `<domain_name>_screenshot_at_<timestamp>.png`.

## Example
To demonstrate how to use this tool, an example CSV file containing URLs (`urls_data.csv`) is provided in the `data/urls/` directory. You can use this file to run the script and capture screenshots of the listed web pages.

## Contributors
- [Pushkar Kathayat](https://github.com/pushkarsingh32)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
