
import cv2
import numpy as np
import os
from os import path

input_file_path = ["/Users/lucky/Desktop/mAP/dark_output/images/",
                   "/Users/lucky/Desktop/mAP/clahe_output/images/",
                   "/Users/lucky/Desktop/mAP/gamma_correction_output/images/",
                   "/Users/lucky/Desktop/mAP/lime_output/images/",
                   "/Users/lucky/Desktop/mAP/retinex_output/images/",
                   "/Users/lucky/Desktop/mAP/enlightenGAN_output/images/"]

# input_file_path = ["/Users/lucky/Desktop/bdd100k/bdd100k_dark/",
#                    "/Users/lucky/Desktop/bdd100k/bdd100k_clahe/",
#                    "/Users/lucky/Desktop/bdd100k/bdd100k_gamma_correction/",
#                    "/Users/lucky/Desktop/bdd100k/bdd100k_lime/",
#                    "/Users/lucky/Desktop/bdd100k/bdd100k_retinex/",
#                    "/Users/lucky/Desktop/bdd100k/bdd100k_enlightenGAN/"]



images_name = os.listdir(input_file_path[0])
R = 0.45 # Please Adjust radio according to your screen

i = 0
while i < len(images_name):
    image_name = images_name[i]

    # Special Condition
    if image_name != 'b249e7f2-d619bd69.jpg':
        i += 1
        continue

    # Check file exist
    for path in input_file_path:
        if not os.path.exists(path + image_name):
            print("File not exist: " + str(path + image_name))

    # read image
    img_0 = cv2.imread(input_file_path[0] + image_name)
    img_1 = cv2.imread(input_file_path[1] + image_name)
    img_2 = cv2.imread(input_file_path[2] + image_name)
    img_3 = cv2.imread(input_file_path[3] + image_name)
    img_4 = cv2.imread(input_file_path[4] + image_name)
    img_5 = cv2.imread(input_file_path[5] + image_name)


    # combine images
    try:
        img_com_012 = np.concatenate((img_0, img_1, img_2), axis=1) # axis = 0 is vertical
        img_com_345 = np.concatenate((img_3, img_4, img_5), axis=1) # axis = 0 is vertical
        img_com = np.concatenate((img_com_012, img_com_345), axis=0) # axis = 0 is vertical
    except Exception as e:
        print(e)
        i += 1
        continue

    # Resize image to make it fit your screen
    img_com = cv2.resize(img_com,
                         (int(img_com.shape[1]*R), int(img_com.shape[0]*R)),
                         interpolation=cv2.INTER_AREA)

    cv2.imshow("Show pair images", img_com)
    print(image_name)
    # Key Event
    key = cv2.waitKey(0) # msec
    if key == ord('q') or key == 27: # Esc or 'q'
        break
    elif key == 44: # '<'
        i -= 1
    else:  # key == 46: # '->'
        i += 1

cv2.destroyAllWindows()