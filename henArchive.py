
## 20230831
import os

import enc
import enc_file

LEN_HEADER = 32

class Archive:
	def __init__(self):
		self.header = b''
		self.mainform = b''
		self.data = b''
		self.ptr = len(self.data)
		self.pwd = None
		self.added_fname = []
	
	def __int2Str(self, i, length):
		str_i = str(i)
		len_i = len(str_i)
		return ' ' * (length - len_i) + str_i
	
	def set_password(self, pwd):
		self.pwd = pwd
	
	def add_file(self, fpath):
		enc_byte = enc_file.encrypt_by_pwd(fpath, self.pwd)
		size = len(enc_byte)
		fname = os.path.basename(fpath)
		if fname in self.added_fname:
			return -1
		self.added_fname.append(fname)
		fname = fname.encode(enc.ENCODING)
		self.mainform += b'|%s?%d?%d' % (fname, self.ptr, self.ptr+size)
		self.data += enc_byte
		self.ptr += size
		self.update_header()
		return 0
	
	def update_header(self):
		enc_main = enc.encrypt_by_pwd(self.mainform, self.pwd)
		self.header = self.__int2Str(len(enc_main), LEN_HEADER).encode(enc.ENCODING)
		return 0
	
	def save(self, fpath):
		enc_header = enc.encrypt_by_pwd(self.header, self.pwd)
		enc_main = enc.encrypt_by_pwd(self.mainform, self.pwd)
		with open(fpath, 'wb') as o:
			o.write(enc_header + enc_main + self.data)

class UnArchive:
	def __init__(self):
		self.header = b''
		self.mainform = b''
		self.mainform_list = []
		self.data = b''
		self.file_data = b''
		self.pwd = None
	
	def load(self, fpath):
		with open(fpath, 'rb') as o:
			self.data  = o.read()
	
	def set_password(self, pwd):
		self.pwd = pwd
	
	def get_header(self):
		self.header = enc.decrypt_by_pwd(self.data[:LEN_HEADER+16], self.pwd)
		return self.header
	
	def get_mainform(self):
		len_main = int(self.header.decode(enc.ENCODING))
		self.mainform = enc.decrypt_by_pwd(self.data[LEN_HEADER+16:LEN_HEADER+16+len_main], self.pwd)
		self.mainform_list = self.list_mainform()
		self.file_data = self.data[LEN_HEADER+16+len_main:]
		return self.mainform_list
	
	def list_mainform(self):
		d_mainform = {}
		l_mainform = self.mainform[1:].split(b'|')
		for f in l_mainform:
			fn, s, e = f.split(b'?')
			d_mainform[fn.decode(enc.ENCODING)] = (int(s), int(e))
		return d_mainform
	
	def extract(self, fname):
		if fname not in self.mainform_list.keys():
			return -1
		s, e = self.mainform_list[fname]
		with open(fname, 'wb') as o:
			o.write(enc.decrypt_by_pwd(self.file_data[s:e], self.pwd))
		return 1

def test_archive():
	ea = Archive()
	ea.set_password('password')
	getstr = None
	while True:
		getstr = input('file: ')
		if getstr == '':
			break
		ea.add_file(getstr)
	ea.save('block.enc')

def test_unarchive():
	ua = UnArchive()
	ua.set_password('password')
	ua.load('block.enc')
	print(ua.get_header())
	print(ua.get_mainform())
	print(ua.list_mainform())
	fn = input('Extract: ')
	ua.extract(fn)
	
if __name__ == '__main__':
#	test_archive()
	test_unarchive()
	