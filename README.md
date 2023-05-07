### VOC 格式转 YOLO txt 格式

- 按如下形式组织目录（注意保持文件夹名称一致）

**root** (whatever you want)

├── **Annotations** (folder)

├   ├── 1.xml

├   ├── 2.xml

├   └── n.xml

├── **JPEGImages** (folder)

├   ├── 1.jpg

├   ├── 2.jpg

├   └── n.jpg

└── **xml2yolo.py** (file)

└── **draw.py** (file)

└── **split_datasets.py** (file)

└── **transform.bat** (file)

- 确保 python 解释器已经添加到环境变量中并且已经安装了 PIL 库
- 双击运行 transform.bat 批处理文件
- 执行成功后，当前目录下将生成 DrawImages 文件夹、labels 文件夹、SplitDataset 文件夹和 classes.txt 文件
- 其中 SplitDataset 文件夹就是最终转换并且划分好的 YOLO txt 格式的数据集（默认按 8:1:1 划分为了 train val test）

------

#### Reference

[Convert PASCAL VOC XML to YOLO for Object Detection](https://towardsdatascience.com/convert-pascal-voc-xml-to-yolo-for-object-detection-f969811ccba5) 

