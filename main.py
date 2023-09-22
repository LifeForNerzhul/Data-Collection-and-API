import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys


def check_import(module_name: str):
    try:
        """
        sys.modules - it is a dictionary that stores information about all modules that have been imported
                      into the current process.
        __name__ - this is a special name that contains the name of the current module.
        """
        getattr(sys.modules[__name__], module_name)
        return True
    except AttributeError:
        return False


def plan_b(site: tuple):
    options = webdriver.FirefoxOptions()
    options.set_preference('dom.webdriver.enabled', False)
    # eager strategy - the main content of the page has loaded and rendered, the user can already interact with it
    options.page_load_strategy = 'eager'
    options.headless = True     # браузер в фоне
    browser = webdriver.Firefox(options=options)
    browser.get(site[1])
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    browser.quit()
    try:
        return site[0](soup)

    except AttributeError:
        return 0


def last_upload(headers: dict):
    """ Get date of last entry in DB
    If for some reason we did not receive a response, then we return the current date

    :param headers: dict with headers to simulate a browser
    :return: str with date as YYYY-MM-DD
    """
    try:
        r = requests.get('https://apex.oracle.com/pls/apex/sokolov_apex/shops_api/get-last-date',
                         headers=headers, timeout=5)
        last_date = r.json().get('items')[0].get('last_upload')
        return last_date[:last_date.find('T'):]
    except:
        return datetime.today().strftime('%Y-%m-%d')


def upload_to_db(shop_name: str, item_price: int, headers: dict):
    """ loading data into my ORACLE DB
    Data is transferred with the URL using the POST method
    If the server returns a code other than 201, then an error message and a response code are displayed
    Only one record can be sent at a time

    :param shop_name:  str with store name
    :param item_price: int
    :param headers: dict with headers to simulate a browser
    """
    # Без headers не проходит
    # И второй вариант
    # payload = { 'shop_name': shop_name, 'price': item_price}
    # r = requests.post('https://apex.oracle.com/pls/apex/sokolov_apex/shops_api/insert', params=payload, headers=headers)
    r = requests.post(
        f'https://apex.oracle.com/pls/apex/sokolov_apex/shops_api/insert?shop_name={shop_name}&price={item_price}',
        headers=headers
    )

    if r.status_code != 201:
        input(f'Ошибка при загрузке в БД, код {r.status_code}')


def get_data(site: tuple, headers: dict, recursion=False):
    """ Get HTML page from site and passes the HTML to the price lookup function, return int price or 0 if failed

    :param site: tuple that contains an indication of the processing function and site link
    :param headers: dict with headers to simulate a browser
    :param recursion: bool Needed to prevent infinite recursion from running
    :return: int price or 0
    """
    try:
        html = requests.get(site[1], headers=headers, timeout=5)
        soup = BeautifulSoup(html.text, 'html.parser')
        return site[0](soup)

    except AttributeError:
        if recursion:
            return 0
        else:
            return get_data(
                site,
                {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0'},
                True)


def ali(soup):
    """ function to find and return int price of item on html page on aliexpress """
    ali_price = soup.find('div', class_='snow-price_SnowPrice__mainS__jlh6el').text.replace('\xa0', '')
    ali_price = ali_price.replace(' ', '')
    return int(ali_price[:ali_price.find(','):])


def bit(soup):
    """ function to find and return int price of item on html page on 28bit.ru """
    return int(soup.find('span', class_="price").text.replace('₽', '').replace(' ', ''))


def xpert(soup):
    """ function to find and return int price of item on html page on xpert.ru """
    return int(soup.find('span', style='font-size:23px;').text)


def compday(soup):
    """ function to find and return int price of item on html page on compday.ru """
    return int(soup.find('b', class_='actual cash price').text.replace(' ', ''))


if __name__ == '__main__':

    browser_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/113.0'}
    site_dict = {
        '28bit': (bit, 'https://28bit.ru/protsessor-amd-ryzen-r5-5500-oem-100-000000457/'),
        'TaiYuan Store': (ali, 'https://aliexpress.ru/item/1005004129008837.html?sku_id=12000028130627271'),
        'cp u Store': (ali, 'https://aliexpress.ru/item/1005004580381433.html?sku_id=12000029704059533'),
        'PYD Store': (ali, 'https://aliexpress.ru/item/1005004806327244.html?sku_id=12000030563931763'),
        'Xpert': (xpert, 'https://www.xpert.ru/products.php?showProduct=191570'),
        'Compday': (compday, 'https://www.compday.ru/komplektuyuszie/protsessory/335378.htm'),
    }

    #   Checking whether the data was entered today or not
    if last_upload(browser_headers) != datetime.today().strftime('%Y-%m-%d'):
        for i in site_dict:
            price = get_data(site_dict.get(i), browser_headers)
            if price == 0:
                if not check_import('webdriver'):
                    from selenium import webdriver
                price = plan_b(site_dict.get(i))
            upload_to_db(i, price, browser_headers)
