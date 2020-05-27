import tensorflow
from tensorflow import keras
from tensorflow.keras import initializers
from tensorflow.keras.models import model_from_json
import os
from PIL import Image
import numpy as np
from io import BytesIO
from yolo import YOLO

# from google.cloud import storag
# GCS_BUCKET = 'sushi-ai-277805.appspot.com'
# DL_FOLDER = '/tmp'
# storage_client = storage.Client()
# bucket = storage_client.get_bucket(GCS_BUCKET)

NETA_CLASS = './model/neta.txt'
NETA_MODEL = './weights/yolo_neta.h5'
SHOP_CLASS = './model/shop.txt'
SHOP_MODEL = './weights/yolo_shop.h5'

class Flag(object):
    def __init__(self):
        self.image = True
        self.input = './path2your_video'
        self.output = ''


class SushiAI():
    def __init__(self, image):
        if image.format is 'PNG':
            bin = BytesIO()
            image.convert('RGB').save(bin, format='jpeg')
            new_image = Image.open(bin)
            self.image = new_image
            del bin, new_image
        else:
            self.image = image

    def getHighestScore(self, list, ratio):
        max = 0
        tmp = ''
        for clss, score in list:
            ans = clss
            ratio.append(f'{ans}: {score:.2%}')
            if score > max:
                max = score
                tmp = ans

        return ans

    def getFileFromGCS(folder):
        path = os.path.join(DL_FOLDER, folder)
        blob = bucket.get_blob(folder)
        blob.download_to_filename(path)
        return path

    def predict(self):
        bin = BytesIO()
        self.image.save(bin, format='jpeg')
        ratio = []
        # class_path = self.getFileFromGCS(NETA_CLASS)
        # model_path = self.getFileFromGCS(NETA_MODEL)
        flag = Flag()
        neta_yolo = YOLO(NETA_CLASS, NETA_MODEL, **vars(flag))
        neta_result = neta_yolo.detect_image(self.image)

        if neta_result == 0:
            return 'しらない', 'おすしです', self.image

        neta = self.getHighestScore(neta_result[1], ratio)

        ratio.append('-----')

        if neta == 'まぐろ':
            # class_path = self.getFileFromGCS(SHOP_CLASS)
            # model_path = self.getFileFromGCS(SHOP_MODEL)
            original = Image.open(bin)
            shop_yolo = YOLO(SHOP_CLASS, SHOP_MODEL, **vars(flag))
            shop_result = shop_yolo.detect_image(original)
            if shop_result == 0:
                return 'しらない', neta, neta_result[1]
            shop = self.getHighestScore(shop_result[1], ratio)
            return_img = shop_result[0]

        else:
            # model_path = self.getFileFromGCS('model/cnn_shop.json')
            # weight_path = self.getFileFromGCS('weights/cnn_shop.hdf5')
            model = model_from_json(open('./model/cnn_shop.json').read())
            model.load_weights('./weights/cnn_shop.hdf5')
            shop_name = ['スシロー', 'はまずし', 'かっぱずし']

            conv_img = neta_result[2].convert('RGB')
            conv_img = conv_img.resize((128, 128), Image.ANTIALIAS)
            img_data = np.asarray(conv_img)
            img_data = np.expand_dims(img_data, axis=0)
            img_data = img_data.astype('float32')
            img_data = img_data / 255.0

            shop_result = model.predict(img_data)
            tmp = shop_result[0]
            for name, score in zip(shop_name, tmp):
                ratio.append(f'{name}: {score:.2%}')
            shop = shop_name[np.argmax(shop_result)]

            return_img = neta_result[0]

        return shop, neta, return_img, ratio
