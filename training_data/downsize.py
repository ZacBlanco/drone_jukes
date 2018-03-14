'''Run this inside an image directory to downscale all images to be lower the MAX_DIM_SIZE
'''
import cv2
import os
import sys
import glob

MAX_DIM_SIZE= 700

def main():
	global MAX_DIM_SIZE
	imlist = glob.glob(os.path.join('.', "*.jpg"))
	try:
		os.mkdir('downsized')
	except OSError as e:
		print("Directory 'downsized' already exists")
		print("Please delete the directory to continue")
	for im in imlist:
		i = cv2.imread(im)
		(rows, cols) = i.shape[:2]
		while rows > MAX_DIM_SIZE and cols > MAX_DIM_SIZE:
			i = cv2.pyrDown(i)
			(rows, cols) = i.shape[:2]
		cv2.imwrite('downsized/{}'.format(im), i)

if __name__ == "__main__":
	main()
