import sys
import henArchive as hac

def make_archive(ha):
	path = None
	path_list = []
	while True:
		path = input('Add file: ')
		if path == '':
			break
		path_list.append(path)
	ha.set_password(input('Set password: '))
	save_name = input('Save as: ')
	for p in path_list:
		ha.add_file(p)
	ha.save(save_name)
	print('Finished.')

def extract(ha):
	ha.set_password(input('Set password: '))
	ha.get_header()
	flist = ha.get_mainform()
	for fn in flist.keys():
		print(fn)
	while True:
		ex_file = input('Extract: ')
		if ex_file == '':
			break
		ha.extract(ex_file)


if __name__ == '__main__':
	if len(sys.argv) == 1:
		ha = hac.Archive()
		make_archive(ha)
	else:
		ha = hac.UnArchive()
		arc_path = sys.argv[1]
		ha.load(arc_path)
		extract(ha)
