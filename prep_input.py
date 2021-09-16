# This code convert result.txt to input/detection-results/
# result.txt is yolov4 model detection output file
import pprint
import os
import json

# TODO 
PROJECT_NAME = "bdd100k_arg_gamma"
RESIZE = False # Switch to True if using DeRainDrop image
result_file = os.path.normpath(os.path.join(os.getcwd(), '../darknet/result_' + PROJECT_NAME + '_daytime.txt'))
out_result_dir = os.path.normpath(os.path.join(os.getcwd(), "input/detection-results"))
out_gt_dir = os.path.normpath(os.path.join(os.getcwd(), "input/ground-truth"))
gt_json = os.path.normpath(os.path.join(os.getcwd(), '../bdd100k/labels/bdd100k_labels_images_val.json'))

################################
### clear target directories ###
################################
for f in os.listdir(out_gt_dir):
  os.remove(os.path.join(out_gt_dir, f))
print("Clean all file in " + out_gt_dir)
for f in os.listdir(out_result_dir):
  os.remove(os.path.join(out_result_dir, f))
print("Clean all file in " + out_result_dir)

###############################################
### Generate detections-result for cartucho ###
###############################################
result_dic = {}
with open(result_file) as result:
  image_name = None
  for line in result:
    if line.find('.jpg') != -1:
      image_name = line.split('.jpg')[0].split('\\')[-1].split('/')[-1] + ".jpg"
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

###############################################
### Generate groundtrue-result for cartucho ###
###############################################

raw_json = json.load(open(gt_json, "r"))
LABEL_MAP = {
    "car": 0,
    "bus": 1,
    "person": 2,
#    "bike": 3,
    "truck": 4,
    # "motor": 5,
    # "train": 6,
    # "rider": 7,
    "traffic sign": 8,
    "traffic light": 9,
}

label = {}
for image_label in raw_json:
  det_list = []
  for det in image_label["labels"]:
    if det["category"] in LABEL_MAP:
      det_list.append((det["category"],
                       round(det["box2d"]['x1']),
                       round(det["box2d"]['y1']),
                       round(det["box2d"]['x2']),
                       round(det["box2d"]['y2'])))
  label[image_label["name"]] = det_list

for name in result_dic:
  with open(os.path.join(out_gt_dir, name.split('.')[0] + '.txt'), 'w') as f:
    for det in label[name]:
      name = None
      if det[0] == 'car' or det[0] == 'truck' or det[0] == 'bus':
        name = 'car'
      elif det[0] == 'traffic light':
        name = 'traffic_light'
      elif det[0] == 'person':
        name = 'person'
      elif det[0] == 'traffic sign':
        name = 'traffic_sign'
      else:
        continue
      if not RESIZE:
        string = name + ' ' + str(det[1]) + ' ' + str(det[2]) + ' ' +\
                str(det[3]) + ' ' + str(det[4]) + '\n'
      else:
        string = name + ' ' + str(det[1]*0.325) + ' ' + str(det[2]*0.57) + ' ' +\
                str(det[3]*0.325) + ' ' + str(det[4]*0.57) + '\n'
      f.write(string)

print("Wrote total " + str(count) + " txt file to " + out_gt_dir)