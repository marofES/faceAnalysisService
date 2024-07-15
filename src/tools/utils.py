# any other non-business logic functions e.g. response normalization, data enrichment, etc.
import cv2
import numpy as np

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