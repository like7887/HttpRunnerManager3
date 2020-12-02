# debugtalk.py
from binascii import b2a_hex
from Crypto.Cipher import AES


def encrypt(text):
    BS = len("cloudwalk2018!@#")
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    key = 'cloudwalk2018!@#'.encode('utf-8')
    mode = AES.MODE_ECB
    cryptos = AES.new(key, mode)
    cipher_text = cryptos.encrypt(bytes(pad(text), encoding="utf8"))
    return b2a_hex(cipher_text)
