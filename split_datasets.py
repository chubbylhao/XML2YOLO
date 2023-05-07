import random
import glob
import os
import shutil


def copyfiles(fil, root_dir):
    basename = os.path.basename(fil)
    filename = os.path.splitext(basename)[0]

    # copy image
    src = fil
    dest = os.path.join(root_dir, generic_image_dir, f"{filename}.jpg")
    shutil.copyfile(src, dest)

    # copy annotations
    src = os.path.join(label_dir, f"{filename}.txt")
    dest = os.path.join(root_dir, label_dir, f"{filename}.txt")
    shutil.copyfile(src, dest)


label_dir = "labels/"
image_dir = "JPEGImages/"
generic_image_dir = "images/"
lower_limit = 0
files = glob.glob(os.path.join(image_dir, '*.jpg'))

# shuffle the files (the file is a list of image paths), no seed, so the result is not reproducible
random.shuffle(files)

folders = {"train": 0.8, "val": 0.1, "test": 0.1}
# below is another split proportion
# folders = {"train": 0.6, "val": 0.2, "test": 0.2}
check_sum = sum([folders[x] for x in folders])
assert check_sum == 1.0, "Split proportion is not equal to 1.0"

split_dir = "SplitDataset/"
if os.path.isdir(split_dir):
    print(f"{split_dir} already exists. Deleting the directory...")
    shutil.rmtree(split_dir)
os.mkdir(split_dir)
print(f"{split_dir} created successfully!")

for folder in folders:
    sub_folder = os.path.join(split_dir, folder)
    os.mkdir(sub_folder)
    print(f"{sub_folder} created successfully!")
    temp_label_dir = os.path.join(sub_folder, label_dir)
    os.mkdir(temp_label_dir)
    temp_image_dir = os.path.join(sub_folder, generic_image_dir)
    os.mkdir(temp_image_dir)

    limit = round(len(files) * folders[folder])
    for fil in files[lower_limit:lower_limit + limit]:
        copyfiles(fil, sub_folder)
    lower_limit = lower_limit + limit
