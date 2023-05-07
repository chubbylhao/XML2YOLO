# 在按VOC格式组织的数据集中，存放所有图片文件的文件夹的名称为JPEGImages，存放所有标注文件的文件夹的名称为Annotations
# 格式转换脚本xml2yolo.py应与JPEGImages文件夹和Annotations文件夹在同一级目录下
#     root
#     ├── Annotations (folder)
#     ├   ├── 1.xml
#     ├   ├── 2.xml
#     ├   └── n.xml
#     ├── JPEGImages (folder)
#     ├   ├── 1.jpg
#     ├   ├── 2.jpg
#     ├   └── n.jpg
#     └── xml2yolo.py

import xml.etree.ElementTree as ET
import glob
import os
import shutil


def xml_to_yolo_bbox(bbox, w, h):
    # xmin, ymin, xmax, ymax
    # --------------------> X (width)
    # | (xmin, ymin) = (bbox[0], bbox[1])
    # |     -----------
    # |     |         |
    # |     |    *    | (x_center, y_center)
    # |     |         |
    # |     -----------
    # |            (xmax, ymax) = (bbox[2], bbox[3])
    # Y (height)
    # YOLO format: class, x_center, y_center, width, height
    # one row per object, class numbers are zero-indexed (start from 0)
    # x_center, y_center, width, height should be normalized to [0, 1]
    # w, h are the width and height of the image
    x_center = ((bbox[2] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[1]) / 2) / h
    width = (bbox[2] - bbox[0]) / w
    height = (bbox[3] - bbox[1]) / h
    return [x_center, y_center, width, height]


# didn't use this function (only for reference)
def yolo_to_xml_bbox(bbox, w, h):
    # x_center, y_center, width, height
    w_half_len = (bbox[2] * w) / 2
    h_half_len = (bbox[3] * h) / 2
    xmin = int((bbox[0] * w) - w_half_len)
    ymin = int((bbox[1] * h) - h_half_len)
    xmax = int((bbox[0] * w) + w_half_len)
    ymax = int((bbox[1] * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]


classes = []
input_dir = "Annotations/"
output_dir = "labels/"  # any name you want
image_dir = "JPEGImages/"

# create the labels' folder (output directory)
if os.path.isdir(output_dir):
    print(f"Output directory {output_dir} already exists. Deleting the directory...")
    shutil.rmtree(output_dir)
os.mkdir(output_dir)
print(f"Output directory {output_dir} created successfully!")

# identify all the xml files in the annotations' folder (input directory)
files = glob.glob(os.path.join(input_dir, '*.xml'))  # or use os.listdir() to get files in a directory
# loop through each
for fil in files:  # for example: fil = "Annotations/1.xml", "Annotations/2.xml", ... (fil is str type)
    basename = os.path.basename(fil)  # for example: basename = "1.xml", "2.xml", ... (basename is str type)
    filename = os.path.splitext(basename)[0]  # for example: filename = "1", "2", ... (filename is str type)
    # check if the label contains the corresponding image file
    if not os.path.exists(os.path.join(image_dir, f"{filename}.jpg")):  # notice the image format, here is jpg
        print(f"{filename}.jpg image does not exist!")
        continue

    result = []

    # parse the content of the xml file
    tree = ET.parse(fil)
    root = tree.getroot()
    width = int(root.find("size").find("width").text)  # get the width of the image
    height = int(root.find("size").find("height").text)  # get the height of the image

    for obj in root.findall('object'):  # all objects must be found
        label = obj.find("name").text
        # check for new classes and append to list
        if label not in classes:  # record all the classes
            classes.append(label)
        index = classes.index(label)  # give the class a number
        pil_bbox = [int(x.text) for x in obj.find("bndbox")]  # for example: [xmin, ymin, xmax, ymax]
        yolo_bbox = xml_to_yolo_bbox(pil_bbox, width, height)
        # convert data to string
        bbox_string = " ".join([str(x) for x in yolo_bbox])
        result.append(f"{index} {bbox_string}")

    if result:  # already parsed one xml file
        # generate a YOLO format text file for each xml file
        with open(os.path.join(output_dir, f"{filename}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(result) + "\n")  # need a new line at the end of the file
    else:  # output warnings if there is no object in the xml file
        print(f"\033[31m Warning \033[0m {filename}.xml has no object!")
print(f"Total {len(files)} xml files processed successfully!")

# generate the classes file as reference
with open('classes.txt', 'w', encoding='utf8') as f:
    for k, v in enumerate(classes):
        f.write(f"{k}: {v}\n")
print(f"Total {len(classes)} classes found and saved in classes.txt!")
