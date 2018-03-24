import gradients
# import hoc here
import hack3 as hoc
from skimage import data
import cv2

import os

def main():

	list_of_files = os.listdir()[:-3]
	f = open("signatures.txt", 'a')

	for i in range(15,34):

		print(list_of_files[i])

		im = cv2.imread(list_of_files[i], 1)

		image, image_s = gradients.preprocess(im)
		
		magnitude, orientation = gradients.find_gradients(image, image_s)
		bins_mat = gradients.bins_in_cells(magnitude, orientation)
		fd_hog = gradients.normalise_and_fd(bins_mat)

		print("after hog")

		arr = hoc.lab_conversion(im)
		fd_hoc = hoc.assignbins(arr)

		print("after hoc")

		final_fd = fd_hog + fd_hoc

		f.write(str(final_fd) + "\n")

		print("YOYOYOYOYOYOYOYOYOYOYOYOYOYOYO")

	f.close()
	
main()