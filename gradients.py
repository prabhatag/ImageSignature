from skimage import color, exposure
import cv2
import numpy as np
import matplotlib.pyplot as plt
# np.set_printoptions(threshold=np.nan)
import math
import scipy

def preprocess(im):

    image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (5, 5), 0)

    image_s = np.asarray(image)
    image_s = np.int8(image)

    return image, image_s


def find_gradients(image, image_s):

    gx = [[-1, 0, 1]]
    gy = [[-1], [0], [1]]
    sy, sx = image.shape

    # WHAT TO DO WITH GRADIENT IMAGE SIZE
    # SHOULD IT BE INT8 OR INT16
    img = np.zeros((sy, sx), dtype = "int16")
    img[:, :2] = image[:, :2]

    # img[:, -2:] = image[:, -2:]

    img[:, 2:] = image_s[:, 2:] - image_s[:, :-2]
    # plt.imshow(img[0:8, 0:8], cmap=plt.cm.Greys_r)
    # plt.show()

    # HOW TO THRESHOLD GRADIENT IMAGE

    img1 = np.zeros((sy, sx), dtype = "int16")
    img1[:2, :] = image[:2, :]
    # img1[-2:, :] = image[-2:, :]
    img1[2:, :] = - image_s[2:, :] + image_s[:-2, :]

    img = np.uint8(np.absolute(img))
    img1 = np.uint8(np.absolute(img1))

    # mag, angle = cv2.cartToPolar(img, img1, angleInDegrees=True)

    magnitude = np.sqrt(img**2 + img1**2)
    orientation = (np.arctan2(img1, img)) * (180 / np.pi)

    return magnitude, orientation

def select_bins(ori, bin_list):

    bin_list = list(bin_list)
    bin1 = min(bin_list, key = lambda x:abs(x-ori))
    bin_list.remove(bin1)

    bin2 = min(bin_list, key = lambda x:abs(x-ori))

    ratio = (ori - bin1) / 20

    return bin1, bin2, ratio

def bins_in_cells(magnitude, orientation):

    cell_size = 8
    n_bins = 9
    sy, sx = magnitude.shape
    bins_mat = [[] for i in range(int(sx/cell_size))]

    for i in range(0, sx, cell_size):
        for j in range(0, sy, cell_size):
            cell_mag = magnitude[i:i+cell_size, j:j+cell_size]
            cell_ori = orientation[i:i+cell_size, j:j+cell_size]
            bins = {0:0, 20:0, 40:0, 60:0, 80:0, 100:0, 120:0, 140:0, 160:0}
            for k in range(cell_size):
                for l in range(cell_size):
                    mag = cell_mag[k, l]
                    ori = int(round(cell_ori[k, l]))
                    bin1, bin2, ratio = select_bins(ori, bins.keys())
                    bins[bin1] = bins[bin1] + mag*ratio
                    bins[bin2] = bins[bin2] + mag*(1 - ratio)
            bins_mat[int(i/cell_size)].append(list(bins.values()))

    bins_mat = np.asarray(bins_mat)

    return bins_mat

def normalise(block_v):
    
    tot_sq = 0
    for i in block_v:
        tot_sq = tot_sq + i**2
    root = math.sqrt(tot_sq)
    for i in range(len(block_v)):
        if root != 0:
            block_v[i] = block_v[i]/root

    return block_v

def normalise_and_fd(bins_mat):

    fd = list()

    bins_mat_y, bins_mat_x, bins_mat_cols = bins_mat.shape 

    for i in range(0, bins_mat_x - 1):
        for j in range(0, bins_mat_y - 1):
            block = bins_mat[i:i+2, j:j+2]
            by, bx, s = block.shape
            block_v = list()
            for k in range(bx):
                for l in range(by):
                    block_v = block_v + list(block[k, l])
            block_v = normalise(block_v)
            fd = fd + block_v

    return fd