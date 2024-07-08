import argparse
import sys
import requests
import cv2
import tensorflow as tf
import numpy as np
import os
from matplotlib import pyplot as plt
import time

import keras
print(tf.__version__)
print(keras.__version__)

from model_load import UltraFaceTF

start_time = time.time()

model_path = "export_models/slim/"
#model = tf.keras.models.load_model(model_path)
model_loading = UltraFaceTF.tf_model_load(model_path)
if model_loading is not None:

    img_path = "imgs/24.jpg"

    img = cv2.imread(img_path)
    h, w, _ = img.shape
    img_resize = cv2.resize(img, (320, 240))
    img_resize = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)
    img_resize = img_resize - 127.0
    img_resize = img_resize / 128.0

    #target_size = (100, 100)

    results = model_loading.predict(np.expand_dims(img_resize, axis=0))  # result=[background,face,x1,y1,x2,y2]
    print(f'results: {results}')


    for i, result in enumerate(results):
        start_x = int(result[2] * w)
        start_y = int(result[3] * h)
        end_x = int(result[4] * w)
        end_y = int(result[5] * h)

        cv2.rectangle(img, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)


    cv2.imwrite(f'imgs/test_output.jpg', img)
    plt.imshow(img)
    plt.axis("off")
    plt.show()

    elapsed_time = time.time() - start_time
    print("Elapsed time:", elapsed_time, "seconds")

else:
    print('TF model is not loading')