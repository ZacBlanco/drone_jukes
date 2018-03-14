import glob
import sys
import os
import argparse


DEFAULT_YOLO_CFG= '''
{}
'''

DEFAULT_OBJ_DATA_CFG = '''
classes= {}
train = {}
valid = {}
names = {}
backup = {}
'''

def create_obj_data_str(classes=1, train='train.txt', valid='valid.txt', names='obj.names', backup='backup/'):
	global DEFAULT_OBJ_DATA_CFG
	return DEFAULT_OBJ_DATA_CFG.format(classes, train, valid, names, backup).strip()

def create_obj_names_file(classnames):
	return '\n'.join([str(classname) for classname in classnames])

def create_train_test(image_dir, percent, train_file, test_file):
	file_train = open(train_file, 'w')
	file_test = open(test_file, 'w')
	counter = 1
	index_test = round(100 / percent)
	for pf in glob.iglob(os.path.join(image_dir, "*.jpg")):
		title, ext = os.path.splitext(pf)
		title = os.path.abspath(title)
		if counter == index_test:
			counter = 1
			file_test.write(title + ext + '\n')
		else:
			file_train.write(title + ext + '\n')
			counter += 1

def create_names_file(filename, names):
	with open(filename, 'w') as f:
		for name in names:
			f.write(name + '\n')

def create_data_file(filename, data):
	with open(filename, 'w') as f:
		f.write(data)

def run(args):
	try:
		os.mkdir(args.cfg_name)
	except:
		pass
	create_train_test(args.im_dir, float(args.test_percent),
			  args.cfg_name + '/' + args.train_file,
			  args.cfg_name + '/' + args.test_file)
	create_names_file(args.cfg_name + '/obj.names', args.classname)
	s = create_obj_data_str(len(args.classname), args.train_file, args.test_file, 'obj.names')
	create_data_file(args.cfg_name + '/obj.data', s)



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('cfg_name', help='A name for this training configuration')
	parser.add_argument('im_dir', help='The directory containing all of your images in .jpg files. Image filenames shoudl match label filenames.')
	parser.add_argument('label_dir', help='The directory containing all of your labels in .txt files. Label filenames should match image filenames.')
	parser.add_argument('-c', '--classname', default=[], action='append', help='Use to associate class names to index values. i.e. the first name corresponds to class 0, then 1, etc..')
	parser.add_argument('-tp', '--test_percent', default='10', help='The percentage of data to use for testing')
	parser.add_argument('-trf', '--train_file', default='train.txt', help='File to put list of training images')
	parser.add_argument('-tef', '--test_file', default='test.txt', help='File to put list of test images')
	a = parser.parse_args()
	run(a)

if __name__ == "__main__":
	main()
