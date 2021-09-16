# This code convert result.txt to input/detection-results/
# result.txt is yolov4 model detection output file

input_result_path = "/Users/lucky/Desktop/VOC07/-1_VOC0712_test/results/"
input_annoated_path = "/Users/lucky/Desktop/VOCdevkit/VOC2007/Annotations/"
image_path = "/Users/lucky/Desktop/VOCdevkit/VOC2007/JPEGImages/"
output_dir_path = "/Users/lucky/Desktop/mAP/tdrn_result_image/"

import pprint
import os 
from collections import defaultdict

THRES = 0.5

# Get result_dic from detection results
file_list = os.listdir(input_result_path)
result_dic = defaultdict(list)
for file_name in file_list:
    class_name = file_name.split('_')[-1].split('.')[0]
    # print(class_name)
    with open(input_result_path + file_name) as f:
        for line in f: # 000067 0.999 45.2 73.2 448.5 212.3
            image_num, conf, x1, y1, x2, y2 = line.split()# [000067, 0.999, 45.2, 73.2, 448.5, 212.3]
            result_dic[image_num].append((class_name, float(conf), float(x1),  float(y1),  float(x2),  float(y2)))
# print(result_dic)

print("Done reading detection results ")
import xml.etree.ElementTree as ET
for img_num in result_dic:
    tree = ET.parse(input_annoated_path + img_num + ".xml")
    root = tree.getroot()
    for obj in root.findall('object'):
        class_name = obj.find('name').text
        bb = obj.find('bndbox')
        result_dic[img_num].append((class_name, "annotate", bb[0].text, bb[1].text, bb[2].text, bb[3].text))

print("Done reading annatation data")

import cv2
# draw image
for i, img_num in enumerate(result_dic):
    img = cv2.imread(image_path + img_num + ".jpg")
    for det in result_dic[img_num]:
        class_name = det[0]
        conf = det[1]
        if conf == "annotate":
            cv2.rectangle(img,
                        (int(det[2]), int(det[3])),
                        (int(det[4]), int(det[5])),
                        (0, 255, 0),
                        2)
        else:
            if conf > THRES:
                cv2.rectangle(img,
                            (int(det[2]), int(det[3])),
                            (int(det[4]), int(det[5])),
                            (0, 0, 255),
                            2)
                cv2.putText(img,
                            class_name + " " + str(round(conf, 2)),
                            (int(det[2]), int(det[3])),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imwrite(output_dir_path + img_num + ".jpg", img)
    print(str(i) + " / " + str(len(result_dic)))
