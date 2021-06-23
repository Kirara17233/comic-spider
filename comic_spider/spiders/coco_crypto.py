import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

mh_info_key = 'fw122587mkertyui'
code_key = 'fw125gjdi9ertyui'
block_size = 16


def decrypt(text):
    mh_info_decipher = AES.new(mh_info_key.encode(), AES.MODE_ECB)
    code_decipher = AES.new(code_key.encode(), AES.MODE_ECB)

    mh_info = unpad(mh_info_decipher.decrypt(base64.b64decode(base64.b64decode(text))), block_size).decode()
    offset = len(':"')

    next = 'enc_code1'
    start = mh_info.find(next) + len(next) + offset
    size = int(unpad(mh_info_decipher.decrypt(base64.b64decode(base64.b64decode(mh_info[start:mh_info.find('"', start)]))), block_size))

    next = 'mhid'
    start = mh_info.find(next, start) + len(next) + offset
    comic_id = int(mh_info[start:mh_info.find('"', start)])

    next = 'enc_code2'
    start = mh_info.find(next, start) + len(next) + offset
    code = unpad(code_decipher.decrypt(base64.b64decode(base64.b64decode(mh_info[start:mh_info.find('"', start)]))), block_size).decode()[6:-1]

    next = 'pagename'
    start = mh_info.find(next, start) + len(next) + offset
    name = mh_info[start:mh_info.find('"', start)]

    next = 'pageurl'
    start = mh_info.find(next, start) + len(next) + offset + 2
    id = int(mh_info[start:mh_info.find('"', start) - 5])

    return comic_id, id, name, size, code
