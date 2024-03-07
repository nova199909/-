import json

import threading
from flask import Flask, render_template, request
from lib.scancore import run_scan
import g_var
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    # run_scan(data['url'], data['dict'], data['cookie'], data['thread'], data['delay'])
    print('app:', id(g_var))
    g_var.thread = threading.Thread(target=run_scan, args=(data['url'], data['dict'], data['cookie'], data['thread'], data['delay'], g_var))
    g_var.thread.start()
    result = {
        'status': 200,
        'message': 'success',
        'data': None
    }
    return result



@app.route('/stop')
def stop():
    # 停止
    g_var.thread.stop()
    g_var.finish = True
    result = {
        'status': 200,
        'message': 'success',
        'data': None
    }
    return result

@app.route('/getWait')
def getWait():
    wait = "请耐心等待3-5分钟，结果一会儿出来"
    result = {
        'status': 200,
        'message': 'success',
        'data': wait
    }
    return result


@app.route('/getProgress')
def getProgress():
    # urls = [
    # ]
    # with open('urls.txt', 'r') as file:
    #     content = file.readlines()
    # for line in content:
    #     urls.apg.urlspend(line)
    g_var.length = len(g_var.url_list) - g_var.start
    url_list = g_var.url_list[g_var.start: g_var.start+g_var.length]
    g_var.start = g_var.start + g_var.length
    status = 201 if g_var.finish else 200
    result = {
        'status': status,
        'message': 'success',
        'data': json.dumps(url_list)
    }
    return result


@app.route('/getResult')
def getResult():
    scan_results = [
        {
            'time': '2023-09-12 10:30:00',
            'url': 'https://example.com',
            'payload': 'Payload 1',
            'vulnerability_type': 'XSS',
        }
    ]
    with open('report.txt', 'r') as file:
        content = file.readlines()

    # 解析每一行数据，并将其添加到字典中
    report_time = ''
    url = ''
    payload = ''
    vulnerability_type = ''
    scan_result = {
        'time': report_time,
        'url': url,
        'payload': payload,
        'vulnerability_type': vulnerability_type,
    }
    for line in content:
        line = line.strip()  # 去除首尾空白字符
        if line.startswith('Report generated at'):
            report_time = line.replace('Report generated at ', '')
        elif line.startswith('URL:'):
            url = line.replace('URL: ', '')
        elif line.startswith('payload:'):
            payload = line.replace('payload: ', '')
        elif line.startswith('漏洞类型：'):
            vulnerability_type = line.replace('漏洞类型：', '')
            scan_result = {
                'time': report_time,
                'url': url,
                'payload': payload,
                'vulnerability_type': vulnerability_type,
            }
            scan_results.append(scan_result)

    # 将结果转换为JSON格式字符串
    #json_data = json.dumps(scan_results, indent=4)
    # 读取report，调成下面的格式。

    # 添加更多结果...
    return render_template('result.html', scan_results=scan_results)


if __name__ == '__main__':
    app.run()
