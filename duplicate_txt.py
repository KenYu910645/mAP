import pprint
import json

int_file = "/Users/lucky/Desktop/mAP/input/b249e7f2-d619bd69.txt"
out_dir = "/Users/lucky/Desktop/mAP/input/ground-truth/"

from shutil import copyfile

new_file_list = ["bilateral_filter_3.txt", "bilateral_filter_5.txt", "bilateral_filter_9.txt",
                 "gaussian_filter_3.txt", "gaussian_filter_5.txt", "gaussian_filter_9.txt",
                 "median_filter_3.txt", "median_filter_5.txt", "median_filter_9.txt",
                 "mean_filter_3.txt", "mean_filter_5.txt", "mean_filter_9.txt",
                 "input_image.txt"]

for i in new_file_list:
    copyfile(int_file, out_dir + i)




