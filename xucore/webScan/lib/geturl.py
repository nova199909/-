import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from get_value.get_value_main import get_value


def get_all_urls(site_url, file_path, value_list, scan_thread, url_cookie, g_var):
    visited_urls = set()  # 记录已访问的 URL
    urls_to_visit = [site_url]  # 待访问的 URL 队列
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Cookie": url_cookie
    }
    while urls_to_visit:
        current_url = urls_to_visit.pop(0)

        if current_url in visited_urls:
            continue

        try:
            response = requests.get(current_url, headers=headers)
        except requests.exceptions.RequestException:
            continue
        flag1 = get_value(current_url, "get", 'small', scan_thread)
        with open(file_path, 'a') as file:
            file.write(current_url + '\n')
        if flag1[0]:
            for p in flag1[1]:
                inject_url = (current_url + "?" + p + "=")
                with open(file_path, 'a') as file:
                    file.write(inject_url + '\n')
                visited_urls.add(inject_url)
        visited_urls.add(current_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        # print(response.text)

        for link in soup.find_all('a'):

            href = link.get('href')
            absolute_url = urljoin(current_url, href)

            # 判断链接是否为站内链接，并且没有被访问过
            if site_url in absolute_url and absolute_url not in visited_urls:
                urls_to_visit.append(absolute_url)
                g_var.url_list.append(absolute_url)
        for link in soup.find_all('frame'):

            href = link.get('src')
            absolute_url = urljoin(current_url, href)

            # 判断链接是否为站内链接，并且没有被访问过
            if site_url in absolute_url and absolute_url not in visited_urls:
                urls_to_visit.append(absolute_url)


        # 获取当前页面的 URL 并保存到文件


def read_urls_from_file(file_path):
    urls = []

    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()  # 去除换行符和空白字符
            urls.append(url)

    return urls

# 调用函数获取站点所有页面的 URL 并保存到文件
