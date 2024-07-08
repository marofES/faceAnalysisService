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

#model_path = "../export_models/slim/"

def tf_model_load(model_path):

    if os.path.exists(model_path):
        print(f"The directory '{model_path}' exists.")
        
        # List the contents of the directory
        contents = os.listdir(model_path)
        print(f"Contents of '{model_path}': {contents}")
        model = tf.keras.models.load_model(model_path)
        return model 
    else:
        print(f"The directory '{model_path}' does not exist.")
        return None 
        


