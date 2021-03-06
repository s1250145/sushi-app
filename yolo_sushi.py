# -*- coding: utf-8 -*-
"""YOLO_sushi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1168_-i1kBOOTsEoPvTDmX_rpXNpCamv1
"""

# !pip install -q tensorflow-gpu==2.0.0-rc1

# Commented out IPython magic to ensure Python compatibility.
# clone yolo project
! git clone https://github.com/qqwweee/keras-yolo3.git
# %cd keras-yolo3

# Commented out IPython magic to ensure Python compatibility.
# make dir for my annotation data
# %mkdir VOCdevkit
# %cd VOCdevkit
# %mkdir VOC2007
# %cd VOC2007

!unzip archive.zip

!rm -f archive.zip
!rm -rf __MACOSX/

! cp ImageSets/Main/test.txt ImageSets/Main/val.txt

# Commented out IPython magic to ensure Python compatibility.
# %cd content/keras-yolo3/

# convert annotation file
!python voc_annotation.py

# make class(label) file
!touch model_data/neta_classes.txt

# !pip install tensorflow-gpu==1.14.0

# download yolov3 model from yolo project
import tensorflow as tf
from tensorflow import keras
!wget https://pjreddie.com/media/files/yolov3.weights

!python convert.py yolov3.cfg yolov3.weights model_data/yolo.h5

# model training
!python train.py

!python yolo_video.py --image