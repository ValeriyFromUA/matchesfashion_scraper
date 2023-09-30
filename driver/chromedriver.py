from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def update_driver() -> Service:
    service = Service(executable_path=ChromeDriverManager().install())
    return service


def get_driver(user_agent) -> webdriver:
    chrome_options = Options()
    chrome_options.add_argument(f'--user-agent={user_agent}')
    chrome_options.add_argument('--window-size=1700,900')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_extension('driver/extensions/extension_1_52_2_0.crx')
    driver = webdriver.Chrome(service=update_driver(), options=chrome_options)
    return driver
