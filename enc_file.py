import sys
import enc

def encrypt_by_pwd(path, pwd):
	with open(path, 'rb') as o:
		return enc.encrypt_by_pwd(o.read(), pwd)

if __name__ == '__main__':
	fname = sys.argv[1]
	with open(fname, 'rb') as o:
		buf = o.read()
	with open('data', 'wb') as o:
		o.write(enc.encrypt_by_pwd(buf, 'password'))