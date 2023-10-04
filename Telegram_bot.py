import requests


file = open('Config.txt', 'r')
file = file.read()
print(file)
file = file.split('\n')
print(file)
config_dict = {}
for i in file:
    print(i.find(': '))
    print(i[:i.find(': '):])
    print(i[i.find(': ') + 2::])
    config_dict.update({i[:i.find(': '):]: i[i.find(': ') + 2::]})
print(config_dict)
print(type(config_dict))

browser_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/113.0'}
db_link = 'https://apex.oracle.com/pls/apex/sokolov_apex/shops_api/diff-between-two-last'
r = requests.get(db_link, headers=browser_headers, timeout=5)
print(r.json().get('items'))
data = r.json().get('items')
message = ''
for item in data:
    message += item.get('shop_name') + ': '
    message += str(item.get('price')) + ', '
    message += str(item.get('price_diff')) + '\n'
print(message)
teleg_link = ''
requests.get(teleg_link, headers=browser_headers, timeout=5)
