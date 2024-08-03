# app/scraper/decryptor.py
import base64
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


class Decryptor:
    def __init__(self):
        self.key = b'57A891D97E332A9D'
        self.iv = b'844182a9dfe9c5ca'

    def decrypt(self, srcs: str) -> str:
        encrypted_data = base64.b64decode(srcs)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        modified_string = re.sub(r'.*akamaized\.net/', 'https://v16m-default.akamaized.net/',
                                 decrypted_data.decode('utf-8'))
        return modified_string
