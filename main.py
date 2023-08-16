import requests
from bs4 import BeautifulSoup


def get_data(site: tuple, headers: dict):
    try:
        html = requests.get(site[1], headers=headers, timeout=5)
        soup = BeautifulSoup(html.text, 'html.parser')
        return site[0](soup)

    except:
        return 0


def ali(soup):
    price = soup.find('div', class_='snow-price_SnowPrice__mainS__jlh6el').text.replace('\xa0', '')
    price = price.replace(' ', '')
    return int(price[:price.find(','):])


def bit(soup):
    return int(soup.find('span', class_="price").text.replace('₽', '').replace(' ', ''))


def xpert(soup):
    return int(soup.find('span', style='font-size:23px;').text)


def compday(soup):
    return int(soup.find('b', class_='actual cash price').text.replace(' ', ''))


browser_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/113.0'}
site_dict = {
    '28bit': (bit, 'https://28bit.ru/protsessor-amd-ryzen-r5-5500-oem-100-000000457/'),
    'TaiYuan Store': (ali, 'https://aliexpress.ru/item/1005004129008837.html?sku_id=12000028130627271'),
    'cp u Store': (ali, 'https://aliexpress.ru/item/1005004580381433.html?sku_id=12000029704059533'),
    'PYD Store': (ali, 'https://aliexpress.ru/item/1005004806327244.html?sku_id=12000030563931763'),

    # 'Xpert': (xpert, 'https://www.xpert.ru/products.php?showProduct=191570'),
    # 'Compday': (compday, 'https://www.compday.ru/komplektuyuszie/protsessory/335378.html'),
}

for i in site_dict:
    print(site_dict.get(i))
    print(get_data(site_dict.get(i), browser_headers))
    print("---------------------------------------------------")
