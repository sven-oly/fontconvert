# Client side-upload of multiple files

import requests

url = "http://127.0.0.1:8080/multiple_upload_test?lang_code=shn"

files = [
    ('files', ('document1.txt', open('document1.txt', 'rb'), 'text/plain')),
    ('files', ('image1.png', open('image1.png', 'rb'), 'image/png'))
]

response = requests.post(url, files=files)
print(response.text)
