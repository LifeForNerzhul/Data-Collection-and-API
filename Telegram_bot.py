import requests


def read_config():
    file = open('Config.txt', 'r')
    file = file.read()
    file = file.split('\n')
    config_dict = {}
    for i in file:
        config_dict.update({i[:i.find(': '):]: i[i.find(': ') + 2::]})
    return config_dict


def get_diff(headers: dict):
    db_link = 'https://apex.oracle.com/pls/apex/sokolov_apex/shops_api/diff-between-two-last'
    r = requests.get(db_link, headers=headers, timeout=5)
    data = r.json().get('items')
    message = ''
    for item in data:
        message += item.get('shop_name') + ': '
        message += str(item.get('price')) + ', '
        message += str(item.get('price_diff')) + '\n'
    return message


def send_message_teleg(config: dict, message: str, headers: dict):
    user_id = config.get('user_id')
    token = config.get('token')
    teleg_link = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={user_id}&text={message}'
    requests.post(teleg_link, headers=headers, timeout=5)


if __name__ == '__main__':
    browser_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/113.0'}
    print(get_diff(browser_headers))
    send_message_teleg(read_config(), get_diff(browser_headers), browser_headers)
