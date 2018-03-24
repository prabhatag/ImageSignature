import cv2
import numpy as np
import itertools
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

def lab_conversion(img):

	# img = cv2.imread('KIabout.PNG', 1)

	hsv_green = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

	lab_pixel_arr = []
	for i in range(len(hsv_green)):
	  temp_arr = []
	  for j in range(len(hsv_green[0])):
	    lab_col = LabColor(hsv_green[i][j][0]/2.55,hsv_green[i][j][1]-128,hsv_green[i][j][2]-128)
	    temp_arr.append(lab_col)
	  lab_pixel_arr.append(temp_arr)

	#cv2.imshow('img', img)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()

	print ("inside lab_conversion")

	return lab_pixel_arr


def assignbins(lab_pixel_arr):

	print("assignbins")

	midpts = []
	x = [-127,0,127]
	mid_pts = [p for p in itertools.product(x, repeat=3)]
	arr_bins = []
	signature_list = []
	for i in range(32):
		#print "a1____"
		for j in range(32):
			l_bin = []

			for x in range(len(mid_pts)):
				a = [mid_pts[x],0]
				l_bin.append(a)
			
			for k in range(8):
				##print "a3____"
				for l in range(8):
					#print "a4____"
					temp_arr = lab_pixel_arr[i*8+k][j*8+l]
					score = 1000
					min_bin = 1000
					for m in range(len(l_bin)):
						if(score > delta_e_cie2000(temp_arr,LabColor(l_bin[m][0][0],l_bin[m][0][1],l_bin[m][0][2]))):
							score = delta_e_cie2000(temp_arr,LabColor(l_bin[m][0][0],l_bin[m][0][1],l_bin[m][0][2]))
							min_bin = m
					#print min_bin
					l_bin[min_bin][1]+=1
					temp_pixel = []
					for x in range(3):
						temp_pixel.append((l_bin[min_bin][0][x]+temp_arr.get_value_tuple()[x])/2)

					temp_pixel = tuple(temp_pixel)
					l_bin[min_bin][0] = temp_pixel
					#print "a____"
			arr_bins.append(l_bin)

	print("after assignbins")

	for i in arr_bins:
		for j in range(len(i)):
			signature_list.append(i[j][1])
	
	return signature_list