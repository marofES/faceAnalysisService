# tools main router with all the endpoints
print(f"tools app is starting")
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

model_path = "D:/faceService/export_models/slim"
#model = tf.keras.models.load_model(model_path)
model_loading = UltraFaceTF.tf_model_load(model_path)

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