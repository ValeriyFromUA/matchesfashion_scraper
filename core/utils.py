import csv
import json
from typing import List

import requests
from colorama import Fore, Style

from core.logger import get_logger

logger = get_logger(__name__)


def data_to_json(data_list: [List], filename: str = 'shoes.json'):
    with open(f"../{filename}", 'w', encoding='utf-8') as json_file:
        json.dump(data_list, json_file, ensure_ascii=False, indent=4)
    logger.info(f"{Fore.GREEN} data saved as {filename} {Style.BRIGHT}")


def data_to_csv(data_list: [List], filename: str = 'shoes.csv'):
    with open(f"../{filename}", 'w', newline='', encoding='utf-8-sig') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=data_list[0].keys(), delimiter=";")
        csv_writer.writeheader()
        csv_writer.writerows(data_list)
    logger.info(f"{Fore.GREEN} data saved as {filename} {Style.BRIGHT}")


def check_security(url):
    response = requests.get(url)
    if response.status_code != 200:
        input('some_poblems')
