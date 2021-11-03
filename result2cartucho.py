# This code convert result.txt to input/detection-results/
# result.txt is yolov4 model detection output file

# TODO
# Input 
src_path = "../darknet/bdd100k_result.txt"
# Output
out_path = "./input/detection-results/"

import pprint
result_dic = {}
with open(src_path) as result:
  image_name = None
  for line in result:
    # It's a loading line
    if line.find('Predicted') != -1:
      image_name = line.split(':')[0].split('/')[-1]
      result_dic[image_name] = []
    
    # It's a detection line
    if line.find('%') != -1:
      s = line.split(':')
      class_name = s[0]
      # class_name = None
      # if s[0] == "traffic light":
      #   class_name = "traffic_light"
      # elif s[0] == "car" or s[0] == "truck":
      #   class_name = "car"
      # elif s[0] == "person":
      #   class_name = "person"
      # else:
      #   continue
      
      confident = int(s[1].split()[0].split('%')[0])/100.0
      left_x = int(s[2].split()[0])
      top_y = int(s[3].split()[0])
      width = int(s[4].split()[0])
      height = int(s[5].split()[0].split(')')[0])
      result_dic[image_name].append((class_name, confident, left_x, top_y, width, height))

# pprint.pprint(result_dic)

# Convert to cartucho format
count = 0
for name in result_dic:
  print("Writing " + name.split('.')[0] + '.txt ....')
  count += 1
  with open(out_path + name.split('.')[0] + '.txt', 'w') as f:
    for det in result_dic[name]:
      string = str(det[0]) + ' ' + str(det[1]) + ' ' + str(det[2]) + ' ' +\
               str(det[3]) + ' ' + str(det[2] + det[4]) + ' ' + str(det[3] + det[5]) + '\n'
      f.write(string)
print("Total " + str(count) + " images")