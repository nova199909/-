import requests


def mode_Jinjia2_linux(url):
    payload = "{{51*51}}"
    get_value = ('/?name=', '/?password=')
    if '=' in url:
        url = url.split('=', 1)[0]+"="
        r = requests.get(url + payload)
        if '2601' in r.text:
            return True, url, payload, 'Template-injection_yes!'
        else:   
            return False, url
    else:
        url = url + '/?name=' + payload;
        r = requests.get(url)
        if '2601' in r.text:
            return True, url, payload, 'Template-injection_yes!'
        else:
            return False, url
