from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

public_key = "pk-pJNAtlAqCHbUDTrDudubjSKeUVgbOMvkRQWMLtscqsdiKmhI"
plaintext = 'api.openkh.org'


def encrypt(public_key, plaintext):
    key = base64.b64decode(public_key.split('-')[1])
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    encoded_ciphertext = public_key + "-" + base64.b64encode(cipher.iv + ciphertext).decode('utf-8')
    return encoded_ciphertext

def decrypt(public_key, encoded_ciphertext):
    key = base64.b64decode(public_key.split('-')[1])
    encoded_ciphertext = encoded_ciphertext.split('-')[1]
    ciphertext = base64.b64decode(encoded_ciphertext)
    iv = ciphertext[:AES.block_size]
    ciphertext = ciphertext[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode('utf-8')