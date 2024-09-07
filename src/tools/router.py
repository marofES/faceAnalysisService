# tools main router with all the endpoints
from fastapi import APIRouter, Depends, HTTPException, status, FastAPI, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
import numpy as np
import cv2
from model_load import UltraFaceTF

from src.auth import schemas, service, dependencies
from src.database import get_session
from src.auth.constants import RoleEnum
from src.tools.utils import *
import base64

import os
import os.path as osp
import argparse
import onnxruntime
from src.tools.scrfd import SCRFD
from src.tools.arcface_onnx import ArcFaceONNX

model_path = "export_models/slim"
#model = tf.keras.models.load_model(model_path)
model_loading = UltraFaceTF.tf_model_load(model_path)

onnxruntime.set_default_logger_severity(3)

assets_dir = osp.expanduser('buffalo_l')

detector = SCRFD(os.path.join(assets_dir, 'det_10g.onnx'))
detector.prepare(0)
model_path = os.path.join(assets_dir, 'w600k_r50.onnx')
rec = ArcFaceONNX(model_path)
rec.prepare(0)

print(f"Model Load Done!! tools app is starting")

router = APIRouter()

@router.post("/face-detect/")
async def face_detect(face_image: UploadFile = File(...)):
    # Read the uploaded file
    contents = await face_image.read()
    if contents is None:
        return {'error': 'Image not uploaded'}
    # Convert file contents to a NumPy array for OpenCV
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    # Process the image
    h, w, _ = img.shape
    img_resize = cv2.resize(img, (320, 240))
    img_resize = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)
    img_resize = img_resize - 127.0
    img_resize = img_resize / 128.0

    
    
    if model_loading is not None:
        results = model_loading.predict(np.expand_dims(img_resize, axis=0))  # result=[background,face,x1,y1,x2,y2]
        #print(f'results: {results}')

        for i, result in enumerate(results):
            start_x, start_y, end_x, end_y = get_coordinates(result, w, h)

            cv2.rectangle(img, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
        resized_img = resize_with_envelope(img, (768, 1024))

        img_base64 = image_to_base64(resized_img)
        
        return JSONResponse(content={"face_image": face_image.filename, "base64_image": img_base64})
    else:
        return {'error': 'TF model is not loading'}


@router.post("/face-detection-and-spilt/")
async def face_detection_and_spilt(face_image: UploadFile = File(...)):
    # Read the uploaded file
    contents = await face_image.read()
    if contents is None:
        return {'error': 'Image not uploaded'}
    # Convert file contents to a NumPy array for OpenCV
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    # Process the image
    h, w, _ = img.shape
    img_resize = cv2.resize(img, (320, 240))
    img_resize = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)
    img_resize = img_resize - 127.0
    img_resize = img_resize / 128.0

    
    
    if model_loading is not None:
        results = model_loading.predict(np.expand_dims(img_resize, axis=0))  # result=[background,face,x1,y1,x2,y2]
        #print(f'results: {results}')
        cropped_img_list = []
        padding = 5
        count = 0


        for i, result in enumerate(results):
            start_x, start_y, end_x, end_y = get_coordinates(result, w, h)

            cropped_img = crop_with_padding(img, start_x, start_y, end_x, end_y, w, h, padding)

            cropped_image_resize = resize_with_envelope(cropped_img, (256, 256))
            cr_base_64 = image_to_base64(cropped_image_resize)
            cropped_img_list.append(cr_base_64)
            
            cv2.rectangle(img, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

            count = count + 1
        
        resized_img = resize_with_envelope(img, (768, 1024))

        original_img = image_to_base64(resized_img)
        
        return JSONResponse(content={"original_image": original_img,"total_face_count": count, "cropped_image_list": cropped_img_list})
    else:
        return {'error': 'TF model is not loading'}
    

@router.post("/face-verify/")
async def face_recognition_and_similarity(face_image_1: UploadFile = File(...), face_image_2: UploadFile = File(...)):
    # Read the uploaded file
    face_1 = await face_image_1.read()
    face_2 = await face_image_2.read()
    if face_1 is None:
        return {'error': 'Image not uploaded'}
    if face_2 is None:
        return {'error': 'Image not uploaded'}

    # Convert byte streams into NumPy arrays for OpenCV
    face_1_np = np.frombuffer(face_1, np.uint8)
    face_2_np = np.frombuffer(face_2, np.uint8)

    # Decode the byte array to OpenCV image format (BGR)
    face_1_img = cv2.imdecode(face_1_np, cv2.IMREAD_COLOR)
    face_2_img = cv2.imdecode(face_2_np, cv2.IMREAD_COLOR)

    bboxes1, kpss1 = detector.autodetect(face_1_img, max_num=1)
    if bboxes1.shape[0]==0:
        return {'error': 'Face not found in Image-1'}
        
    bboxes2, kpss2 = detector.autodetect(face_2_img, max_num=1)
    if bboxes2.shape[0]==0:
        return {'error': 'Face not found in Image-2'}
    # Extract the keypoints/landmarks from the detection
    kps1 = kpss1[0] if kpss1 is not None and len(kpss1) > 0 else None
    kps2 = kpss2[0] if kpss2 is not None and len(kpss2) > 0 else None
    # Ensure that keypoints are not None before proceeding
    if kps1 is None or kps2 is None:
        return {'error': 'Landmarks (keypoints) not detected'}
    
    feat1 = rec.get(face_1_img, kps1)
    feat2 = rec.get(face_2_img, kps2)
    sim = rec.compute_sim(feat1, feat2)
    if sim<0.2:
        conclu = 'They are NOT the same person'
    elif sim>=0.2 and sim<0.28:
        conclu = 'They are LIKELY TO be the same person'
    else:
        conclu = 'They ARE the same person'
    
    print(f"sim: {sim} and conclu: {conclu}")
    sim_rounded = round(float(sim), 4)
        
    return JSONResponse(content={"sim": sim_rounded,"msg": conclu})