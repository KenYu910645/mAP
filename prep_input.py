# This code convert result.txt to input/detection-results/
# result.txt is yolov4 model detection output file
import pprint
import os
import json
import glob
from shutil import rmtree, copyfile

# TODO 
RESIZE = False # Switch to True if using DeRainDrop image
# Input 
result_file = "../darknet/bdd100k_test_only_daytime_result.txt"
images_dir = "../bdd100k_all/test_only_daytime/"
# BDD100K legecy
# gt_json = os.path.normpath(os.path.join(os.getcwd(), '../bdd100k/labels/bdd100k_labels_images_val.json'))
# BDD100k
ano_path = "../bdd100k_all/test_only_daytime/"
# KITTI
# ano_path = "/home/spiderkiller/Desktop/kitti_dataset/label_2/"
# Output
out_result_dir = "./input/detection-results/"
out_gt_dir = "./input/ground-truth/"
out_image_dir = "./input/images/"
################################
### clear target directories ###
################################
# Clear output directory
for i in [out_result_dir, out_gt_dir, out_image_dir]:
    print("Cleaning output dir : " + i)
    rmtree(i, ignore_errors=True)
    os.mkdir(i)

###############################################
### Generate detections-result for cartucho ###
###############################################
result_dic = {}
with open(result_file) as result:
    image_name = None
    for line in result:
        if line.find('Predicted') != -1:
            # image_name = line.split('.jpg')[0].split('\\')[-1].split('/')[-1] + ".jpg"
            image_name = os.path.split(line.split()[0])[1]
            result_dic[image_name] = []

        # It's a detection line
        if line.find('%') != -1:
            s = line.split(':')
            class_name = s[0]
            
            confident = int(s[1].split()[0].split('%')[0])/100.0
            left_x = int(s[2].split()[0])
            top_y = int(s[3].split()[0])
            width = int(s[4].split()[0])
            height = int(s[5].split()[0].split(')')[0])
            result_dic[image_name].append((class_name, confident, left_x, top_y, width, height))

# Convert to cartucho format
count = 0
for name in result_dic:
    count += 1
    with open(os.path.join(out_result_dir, name.split('.')[0] + '.txt'), 'w') as f:
        for det in result_dic[name]:
            string = str(det[0]) + ' ' + str(det[1]) + ' ' + str(det[2]) + ' ' +\
                             str(det[3]) + ' ' + str(det[2] + det[4]) + ' ' + str(det[3] + det[5]) + '\n'
            f.write(string)
print("Wrote total " + str(count) + " txt file to " + out_result_dir)

####################################
### Generate images for cartucho ###
####################################

print("Copying images from " + images_dir + " to " + out_image_dir)
for fn in glob.glob(images_dir + "*.jpg") + glob.glob(images_dir + "*.png"):
    copyfile(fn, out_image_dir + fn.split('/')[-1])

###############################################
### Generate groundtrue-result for cartucho ### (BDD100K)
###############################################
LABEL_MAP = {
    0 : "car",
    1 : "person",
    2 : "traffic_sign",
    3 : "traffic_light"
}

(W, H) = (1280, 720)
for fn in glob.glob(ano_path + '*.txt'):
    with open(fn, 'r') as f_input:
        s = ""
        lines = f_input.readlines()
        for l in lines:
            class_num, cx, cy, w, h = [float(i) for i in l.split()]
              
            # if det[0] in LABEL_MAP:
            x1 = str( int( (2*cx - w)*(W/2) ) )
            x2 = str( int( (2*cx + w)*(W/2) ) )
            y1 = str( int( (2*cy - h)*(H/2) ) )
            y2 = str( int( (2*cy + h)*(H/2) ) )

            s += LABEL_MAP[int(class_num)] + " " + x1 + " " + y1 + " " + x2 + " " + y2 + '\n'
        with open(out_gt_dir + fn.split('/')[-1], 'w') as f_output:
            f_output.write(s)


###############################################
### Generate groundtrue-result for cartucho ### (KITTI)
###############################################
# LABEL_MAP = {
#     'Car' : 0,
#     'Pedestrian' : 1,
#     'Cyclist' : 2
# }

# for file in os.listdir(ano_path):
#     with open(ano_path + file, 'r') as f_input:
#         s = ""
#         lines = f_input.readlines()
#         for l in lines:
#             det = l.split()
#             if det[0] in LABEL_MAP:
#                 s += det[0] + " " + det[4] + " " + det[5] + " " + det[6] + " " + det[7] + '\n'
#         with open(out_gt_dir + file, 'w') as f_output:
#             f_output.write(s)

###############################################
### Generate groundtrue-result for cartucho ### (BDD100K legecy)
###############################################

# raw_json = json.load(open(gt_json, "r"))
# LABEL_MAP = {
#         "car": 0,
#         "bus": 1,
#         "person": 2,
# #        "bike": 3,
#         "truck": 4,
#         # "motor": 5,
#         # "train": 6,
#         # "rider": 7,
#         "traffic sign": 8,
#         "traffic light": 9,
# }

# label = {}
# for image_label in raw_json:
#     det_list = []
#     for det in image_label["labels"]:
#         if det["category"] in LABEL_MAP:
#             det_list.append((det["category"],
#                                                round(det["box2d"]['x1']),
#                                                round(det["box2d"]['y1']),
#                                                round(det["box2d"]['x2']),
#                                                round(det["box2d"]['y2'])))
#     label[image_label["name"]] = det_list

# for name in result_dic:
#     with open(os.path.join(out_gt_dir, name.split('.')[0] + '.txt'), 'w') as f:
#         for det in label[name]:
#             name = None
#             if det[0] == 'car' or det[0] == 'truck' or det[0] == 'bus':
#                 name = 'car'
#             elif det[0] == 'traffic light':
#                 name = 'traffic_light'
#             elif det[0] == 'person':
#                 name = 'person'
#             elif det[0] == 'traffic sign':
#                 name = 'traffic_sign'
#             else:
#                 continue
#             if not RESIZE:
#                 string = name + ' ' + str(det[1]) + ' ' + str(det[2]) + ' ' +\
#                                 str(det[3]) + ' ' + str(det[4]) + '\n'
#             else:
#                 string = name + ' ' + str(det[1]*0.325) + ' ' + str(det[2]*0.57) + ' ' +\
#                                 str(det[3]*0.325) + ' ' + str(det[4]*0.57) + '\n'
#             f.write(string)

# print("Wrote total " + str(count) + " txt file to " + out_gt_dir)
