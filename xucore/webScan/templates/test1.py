
urls = [
    'https://www.baidu.com',
    'https://www.taobao.com',
    'https://www.jd.com',
    'https://www.163.com',
    'https://www.qq.com'
]
with open('../urls.txt', 'r') as file:
    content = file.readlines()
for line in content:
    urls.append(line)
print(urls)