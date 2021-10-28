import pprint
import json
RESIZE = False # Switch to True if using DeRainDrop image
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
out_dir = "/Users/lucky/Desktop/mAP/input/ground-truth/"
raw_json = json.load(open("/Users/lucky/Desktop/bdd100k/labels/bdd100k_labels_images_val.json", "r"))

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

for name in label:
  # if name.split('.')[0] != "b249e7f2-d619bd69":
  #   continue
  print("Writing " + name.split('.')[0] + '.txt ....')
  with open(out_dir + name.split('.')[0] + '.txt', 'w') as f:
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
