import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

mh_info_key = 'fw122587mkertyui'
code_key = 'fw125gjdi9ertyui'
block_size = 16


def decrypt(text):
    mh_info_decipher = AES.new(mh_info_key.encode(), AES.MODE_ECB)
    mh_info = unpad(mh_info_decipher.decrypt(base64.b64decode(base64.b64decode(text))), block_size).decode()
    start = mh_info.find('enc_code1') + 11
    size = int(unpad(mh_info_decipher.decrypt(base64.b64decode(base64.b64decode(mh_info[start:mh_info.find('"', start)]))), block_size))
    start = mh_info.find('mhid', start) + 6
    comic_id = int(mh_info[start:mh_info.find('"', start)])
    start = mh_info.find('enc_code2', start) + 11
    code_decipher = AES.new(code_key.encode(), AES.MODE_ECB)
    code = unpad(code_decipher.decrypt(base64.b64decode(base64.b64decode(mh_info[start:mh_info.find('"', start)]))), block_size).decode()[6:-1]
    start = mh_info.find('mhname', start) + 8
    name = mh_info[start:mh_info.find('"', start)]
    start = mh_info.find('pageurl', start) + 11
    id = int(mh_info[start:mh_info.find('"', start) - 5])
    return comic_id, id, name, size, code
