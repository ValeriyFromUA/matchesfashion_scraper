import random
import time
from typing import Dict, List

from bs4 import BeautifulSoup
from colorama import Fore, Style
from fake_useragent import UserAgent
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from core.config import BASE_URLS, CARDS_ON_PAGE
from core.logger import get_logger
from core.utils import data_to_csv, data_to_json
from driver.chromedriver import get_driver

user_agent = UserAgent()

logger = get_logger(__name__)
driver = get_driver(user_agent.random)


def wait_for_page_to_load():
    return driver.execute_script("return document.readyState") == "complete"


def get_categories() -> List[Dict]:
    category_urls = []
    for url in BASE_URLS:
        time.sleep(random.uniform(2, 6))
        driver.get(url)
        driver.refresh()
        time.sleep(random.uniform(2, 6))
        soup = BeautifulSoup(driver.page_source, 'lxml')
        categories = soup.find_all('a', class_='css-1n47t96')
        category_urls.extend(
            [{f"{category.text}": f"https://www.matchesfashion.com{category['href']}"} for category in categories])
    logger.info(f"{Fore.GREEN} Collected categories {Style.BRIGHT}")
    return category_urls


def get_page_count(page_source: str):
    time.sleep(random.uniform(2, 6))
    soup = BeautifulSoup(page_source, 'lxml')
    results = soup.find('div', class_='css-1cg9o3l')
    if results:
        page_count = int(results.text.split()[0]) // CARDS_ON_PAGE
        return page_count


def get_category_data(category_url: str, product_category: str):
    try:
        card_data = []
        driver.get(category_url)
        page_count = get_page_count(driver.page_source)

        for _ in range(page_count):
            time.sleep(random.uniform(2, 6))
            driver.execute_script("window.scrollBy(0, 300);")
            WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.CLASS_NAME, "css-15ylk4w"))).click()
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            driver.execute_script("window.scrollBy(0, -700);")
            wait_for_page_to_load()
            logger.info(
                f"{Fore.GREEN} Scrolling through page no.{_ + 1}/{page_count} {product_category} {Style.BRIGHT}")
        time.sleep(random.uniform(2, 6))
        soup = BeautifulSoup(driver.page_source, 'lxml')
        cards = soup.find_all('div', class_='css-1kxonj9')
        for card in cards:
            data = {
                'title': card.find('p', class_='chakra-text css-13hd2r4').text,
                'url': f"https://www.matchesfashion.com{card.find('a', class_='chakra-link css-nnzi91')['href']}",
                'price': card.find('span', class_='chakra-text css-1cf9vlj').text.replace('£', ''),
                'price_drop': None,
                'image_url': card.find('img', class_='css-s08p0c')['src'].replace('//', '') if card.find('img',
                                                                                                         class_='css-s08p0c') else None,
                'category': product_category,
                'gender': 'women' if '/womens/' in category_url else 'man',

            }
            card_data.append(data)
        logger.info(f"{Fore.GREEN} Collected {product_category} {Style.BRIGHT}")
        return card_data
    except Exception as e:
        logger.info(f"{Fore.YELLOW}  {e} {Style.BRIGHT}")


def get_all_product():
    logger.info(f"{Fore.GREEN} *** Start of data collection ***{Style.BRIGHT}")
    data = []
    categories = get_categories()
    for category in categories:
        time.sleep(random.uniform(10, 20))
        for product_category, category_url in category.items():
            try:
                data.extend(get_category_data(category_url=category_url, product_category=product_category))
            except Exception as e:
                logger.info(f"{Fore.YELLOW}  {e} {Style.BRIGHT}")
                continue

    data_to_csv(data)
    data_to_json(data)
    logger.info(f"{Fore.GREEN} *** All data collected *** {Style.BRIGHT}")
    return data
