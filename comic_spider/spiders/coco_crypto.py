import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

mh_info_key = 'fw122587mkertyui'
code_key = 'fw125gjdi9ertyui'
block_size = 16


def decrypt(text):
    mh_info_decipher = AES.new(mh_info_key.encode(), AES.MODE_ECB)
    mh_info = unpad(mh_info_decipher.decrypt(base64.b64decode(base64.b64decode(text))), block_size).decode()
    start = mh_info.find('enc_code2') + 11
    code_decipher = AES.new(code_key.encode(), AES.MODE_ECB)
    return unpad(code_decipher.decrypt(base64.b64decode(base64.b64decode(mh_info[start:mh_info.find('"', start)]))), block_size).decode()[6:-1]
