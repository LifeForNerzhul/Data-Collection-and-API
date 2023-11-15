import requests
from datetime import datetime
import json
import os


def get_backup_data(headers: dict, link: str):
    return requests.get(link, headers=headers, timeout=10).json().get('items')


def read_access_key():
    try:
        return open('Backup\\access.txt', 'r').read()
    except FileNotFoundError:
        return open('access.txt', 'r').read()


def get_current_date():
    return datetime.today().date()


def write_json(backup_data, date):
    with open(f"{date}.json", "w") as f:
        json.dump(backup_data, f)


def check_day_and_file(date):
    if date.day in (1, 15) and not os.path.exists(f"{date}.json"):
        return True
    else:
        return False


def check_dir():
    cur_folder = os.getcwd()
    cur_folder = cur_folder[cur_folder.rfind('\\') + 1::]
    if cur_folder != 'Backup':
        os.chdir(os.getcwd() + '\\Backup')


def make_backup():
    current_date = get_current_date()
    check_dir()
    if check_day_and_file(current_date):
        browser_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/113.0'}
        backup_data = get_backup_data(browser_headers, read_access_key())
        write_json(backup_data, current_date)


if __name__ == '__main__':
    make_backup()
