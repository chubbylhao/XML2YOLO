@echo off
REM 按序执行3个脚本（默认 python 解释器已经添加到环境变量中）
REM 需要PIL库，使用 pip install Pillow 命令进行安装
@echo on
python xml2yolo.py
python draw.py
python split_datasets.py
pause
