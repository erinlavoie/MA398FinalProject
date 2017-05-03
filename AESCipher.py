# Erin Lavoie, Pearson Treanor, Nick Cameron
# MA398
# AESCipher.py: Code inspired by code @ repo : https://gist.github.com/forkd/168c9d74b988391e702aac5f4aa69e41

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random as rand
import base64
import pickle

def get_random_key():
    return rand.get_random_bytes(AES.block_size)

def pad(s):
    return s + (AES.block_size - len(s) % AES.block_size) * '{'


def unpad(s):
    return s.strip('{')


def encrypt(secret, message):
    if type(message) is str:
        raw = pad(message)
    else:
        raw = message
    iv = rand.new().read(AES.block_size)
    cipher = AES.new(secret, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))


def decrypt(secret, ciphertext):
    enc = base64.b64decode(ciphertext)
    iv = enc[:16]
    cipher = AES.new(secret, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]).decode('utf-8'))


rsa = RSA.generate(2048)
pub = rsa.publickey()
mes = pickle.dumps(pub)

recpub = pickle.loads(mes)

aeskey = get_random_key()

ciphertext = recpub.encrypt(aeskey, 32)[0]

plaintext = rsa.decrypt(ciphertext)

print(aeskey)
print(plaintext)

