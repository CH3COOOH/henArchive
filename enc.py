## pycryptodome
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib

STD_AES_MODE = AES.MODE_EAX
STD_HASH = hashlib.sha256
LEN_SAULT = 16
ENCODING = 'utf-8'

def hash_byte(data):
	return STD_HASH(data).digest()

def pwd_to_key(pwd):
	return hash_byte(pwd.encode(ENCODING))

def encrypt_byte(data, k):
	sault = get_random_bytes(LEN_SAULT)
	cipher = AES.new(k, STD_AES_MODE, nonce=sault)
	ciphertext = cipher.encrypt(data)
	return sault + ciphertext
	
def encrypt_by_pwd(data, pwd):
	k = pwd_to_key(pwd)
	return encrypt_byte(data, k)

def decrypt_byte(data, k):
	nc = data[:LEN_SAULT]
	cipher = AES.new(k, STD_AES_MODE, nonce=nc)
	return cipher.decrypt(data[LEN_SAULT:])

def decrypt_by_pwd(data, pwd):
	k = pwd_to_key(pwd)
	return decrypt_byte(data, k)

if __name__ == '__main__':
	p = 'password'
	# s = 'date: 2023/08/30'
	# length = 16 + N
	s = '00'
	ct = encrypt_by_pwd(s.encode(), p)
	dt = decrypt_by_pwd(ct, p).decode()
	print(s)
	print(ct)
	print(len(ct))
	print(dt)
	