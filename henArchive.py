
## 20230831
import os

import enc
import enc_file

LEN_HEADER = 8
LEN_APPEND = 16

## |1.header|2.mainform|3.data|
## 1. header: length of 2.
## 2. mainform: file list, "fname?sp?ep|fname?sp?ep|fname?sp?ep"
## 3. data: real payload

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
		if self.mainform == b'':
			self.mainform += b'%s?%d?%d' % (fname, self.ptr, self.ptr+size)
		else:
			self.mainform += b'|%s?%d?%d' % (fname, self.ptr, self.ptr+size)
		self.data += enc_byte
		self.ptr += size
		self.update_header()
		return 0
	
	def update_header(self):
		enc_main = enc.encrypt_by_pwd(self.mainform, self.pwd)
		# self.header = self.__int2Str(len(enc_main), LEN_HEADER).encode(enc.ENCODING)
		self.header = len(enc_main).to_bytes(LEN_HEADER, 'big')
		return 0
	
	def save(self, fpath):
		enc_header = enc.encrypt_by_pwd(self.header, self.pwd)
		enc_main = enc.encrypt_by_pwd(self.mainform, self.pwd)
		with open(fpath, 'wb') as o:
			o.write(enc_header + enc_main + self.data)

class UnArchive:
	def __init__(self):
		self.header = None
		self.mainform_row = None
		self.mainform = None
		self.raw_data = None
		self.file_data = None
		self.pwd = None
		self.isUnpacked = False
		self.sp = [-1, -1]
	
	def load(self, fpath):
		with open(fpath, 'rb') as o:
			self.raw_data  = o.read()
	
	def set_password(self, pwd):
		self.pwd = pwd
	
	def __update_spoints(self):
		self.sp[0] = LEN_HEADER+LEN_APPEND
		self.header = enc.decrypt_by_pwd(self.raw_data[ : self.sp[0]], self.pwd)
		self.sp[1] = self.sp[0] + int.from_bytes(self.header, 'big')

	def __update_mainform(self):
		self.mainform = {}
		l_mainform = self.mainform_row.split(b'|')
		for f in l_mainform:
			fn, s, e = f.split(b'?')
			self.mainform[fn.decode(enc.ENCODING)] = (int(s), int(e))
	
	def get_header(self):
		return self.header
	
	def unpack(self):
		if self.pwd == None:
			return -1
		self.__update_spoints()
		self.mainform_row = enc.decrypt_by_pwd(self.raw_data[self.sp[0] : self.sp[1]], self.pwd)
		self.__update_mainform()
		self.file_data = self.raw_data[self.sp[1] : ]
		self.isUnpacked = True
		return self.mainform

	def get_mainform(self):
		return self.mainform

	def extract(self, fname):
		if fname not in self.mainform.keys():
			return -1
		s, e = self.mainform[fname]
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
	ua.load('block.enc')
	ua.set_password('password')
	print(ua.unpack())
	fn = input('Extract: ')
	ua.extract(fn)
	
if __name__ == '__main__':
	# test_archive()
	test_unarchive()
	