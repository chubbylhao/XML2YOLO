# draw.py脚本应该在xml2yolo.py脚本执行之后再执行
# draw.py脚本应该与JPEGImages文件夹和labels文件夹在同一级目录下
#     root
#     ├── JPEGImages (folder)
#     ├   ├── 1.jpg
#     ├   ├── 2.jpg
#     ├   └── n.jpg
#     ├── labels (folder)
#     ├   ├── 1.txt
#     ├   ├── 2.txt
#     ├   └── n.txt
#     └── draw.py

from PIL import Image, ImageDraw
import os
import shutil


def yolo_to_xml_bbox(bbox, w, h):
    # x_center, y_center width height
    w_half_len = (bbox[2] * w) / 2
    h_half_len = (bbox[3] * h) / 2
    xmin = int((bbox[0] * w) - w_half_len)
    ymin = int((bbox[1] * h) - h_half_len)
    xmax = int((bbox[0] * w) + w_half_len)
    ymax = int((bbox[1] * h) + h_half_len)
    return [xmin, ymin, xmax, ymax]


def draw_image(img, bboxes, save_path=None):
    draw = ImageDraw.Draw(img)
    for bbox in bboxes:
        draw.rectangle(bbox, outline="red", width=2)
    img.save(save_path)  # save the image with bounding boxes
    # img.show()  # show the image with bounding boxes (too many to show)


image_dir = "JPEGImages/"
label_dir = "labels/"
image_files = os.listdir(image_dir)  # for example: image_file = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg']
label_files = os.listdir(label_dir)  # for example: label_file = ['1.txt', '2.txt', '3.txt', '4.txt', '5.txt']

assert len(image_files) == len(label_files), "The number of images and labels are not equal."
draw_output_dir = "DrawImages/"
if os.path.isdir(draw_output_dir):
    print("The DrawImages folder already exists, so it will be deleted and recreated.")
    shutil.rmtree(draw_output_dir)
os.mkdir(draw_output_dir)
print("DrawImages folder created successfully!")

for image_file, label_file in zip(image_files, label_files):
    assert os.path.splitext(image_file)[0] == os.path.splitext(label_file)[0], \
        f"The {image_file} and {label_file} file names are not equal."
    image_path = os.path.join(image_dir, image_file)
    label_path = os.path.join(label_dir, label_file)
    bboxes = []
    img = Image.open(image_path)
    with open(label_path, 'r', encoding='utf8') as f:
        for line in f:
            data = line.strip().split(' ')
            bbox = [float(x) for x in data[1:]]
            bboxes.append(yolo_to_xml_bbox(bbox, img.width, img.height))
    draw_image(img, bboxes, os.path.join(draw_output_dir, image_file))
print("Draw images successfully! Total number of images:", len(image_files))
