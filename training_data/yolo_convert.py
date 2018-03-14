import cv2
import os
import sys
import glob

CONVERTED_DIRNAME = 'yolo_labels'

def main():
	global CONVERTED_DIRNAME
	try:
		os.mkdir(CONVERTED_DIRNAME)
	except:
		pass
	CURDIR = os.path.abspath(os.getcwd())
	img_files = glob.glob(os.path.join(CURDIR,"*.jpg"))
	#print(img_files)
	for img_file in img_files:
		(cd, fname) = os.path.split(img_file)
		fileid = fname[:-4]
		labelname = fileid + '.txt'
		s = ''
		img = cv2.imread(img_file)
		height, width = img.shape[:2]
		with open(labelname, 'r') as f:
			s = ' '.join(f.readlines()).replace('\n', '')
		vals = [int(x) for x in s.split(' ')]
		newvals = [0]*5
		newvals[0] = vals[0] - 1
		newvals[1] = float(vals[1] + vals[3])/(2*width)
		newvals[2] = float(vals[2] + vals[4])/(2*height)
		newvals[3] = float(vals[3] - vals[1])/width
		newvals[4] = float(vals[4] - vals[2])/height
		#print(' '.join([str(x) for x in vals]))
		fline = ' '.join([str(x) for x in newvals])
		newfilename = os.path.join(CURDIR, CONVERTED_DIRNAME)
		newfilename = os.path.join(newfilename, labelname)
		#print(newfilename)
		with open(newfilename, 'w') as f:
			f.write(fline + '\n')


if __name__ == "__main__":
	main()
