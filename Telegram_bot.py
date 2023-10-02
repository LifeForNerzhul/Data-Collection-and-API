f = open('Config.txt', 'r')
f = f.read()
print(f)
f = f.split('\n')
print(f)
config_dict = {}
for i in f:
    print(i.find(': '))
    print(i[:i.find(': '):])
    print(i[i.find(': ') + 2::])
    config_dict.update({i[:i.find(': '):]: i[i.find(': ') + 2::]})
print(config_dict)
print(type(config_dict))

