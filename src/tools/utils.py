# any other non-business logic functions e.g. response normalization, data enrichment, etc.
import cv2
import numpy as np
import base64

def resize_with_envelope(image, target_size=(768, 1024)):
    h, w = image.shape[:2]
    target_h, target_w = target_size

    # Compute the aspect ratio of the image and target
    aspect_ratio = w / h
    target_aspect_ratio = target_w / target_h

    # Determine new dimensions based on aspect ratio
    if aspect_ratio > target_aspect_ratio:
        new_w = target_w
        new_h = int(target_w / aspect_ratio)
    else:
        new_h = target_h
        new_w = int(target_h * aspect_ratio)

    # Resize the image
    resized_image = cv2.resize(image, (new_w, new_h))

    # Create a black canvas of target size
    canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)

    # Compute top-left corner coordinates to place the resized image on the canvas
    x_offset = (target_w - new_w) // 2
    y_offset = (target_h - new_h) // 2

    # Place the resized image on the canvas
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized_image

    return canvas


def image_to_base64(image):
    # Convert the processed image to base64
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')


def get_coordinates(result, w, h):
    start_x = int(result[2] * w)
    start_y = int(result[3] * h)
    end_x = int(result[4] * w)
    end_y = int(result[5] * h)
    return start_x, start_y, end_x, end_y


def crop_with_padding(img, start_x, start_y, end_x, end_y, w, h, padding=5):
    ap_start_x = max(0, start_x - padding)
    ap_start_y = max(0, start_y - padding)
    ap_end_x = min(w, end_x + padding)
    ap_end_y = min(h, end_y + padding)
    return img[ap_start_y:ap_end_y, ap_start_x:ap_end_x]