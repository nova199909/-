#!/usr/bin/env python
# coding=utf8

import requests
from .geturl import get_all_urls, read_urls_from_file
from report.report import generate_report
from payload.xxe.xee import mode_xxe_windows, mode_xxe_linux
from payload.fileinclude.fileInclude import mode_fileInclude
from payload.fdownload.fdownload import mode_down
from payload.unload.upload import mode_fupload
from payload.ssrf.ssrf import check_ssrf
from bs4 import BeautifulSoup
import time


def run_scan(urlname, dict_value, cookie, thread, delay, g_var):
    thread = 10
    cookie = ''
    delay = 0
    g_var.url_list.append('开始扫描···')


    get_all_urls(urlname, "urls.txt", dict_value, thread, cookie, g_var)  # 遍历目录
    url_list = read_urls_from_file('urls.txt')
    g_var.url_list.append('开始扫描···')
    for url in url_list:
        print('url:', url)
        g_var.url_list.append(url)
        time.sleep(delay)
        if mode_fileInclude(url, cookie)[0]:
            generate_report(mode_fileInclude(url, cookie))
        elif mode_down(url)[0]:
            generate_report(mode_down(url))
        elif mode_xxe_windows(url)[0]:
            generate_report(mode_xxe_windows(url))
        elif mode_fupload(url)[0]:
            generate_report(mode_fupload(url))
        elif check_ssrf(url)[0]:
            generate_report(check_ssrf(url))
    g_var.finish = True