"""
Utility functions for truck tracking system.
"""

import cv2
import numpy as np
from pathlib import Path


def load_image(image_path):
    """Load image from file."""
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
    return image


def save_image(image, output_path):
    """Save image to file."""
    cv2.imwrite(str(output_path), image)
    print(f"Image saved to {output_path}")


def resize_image(image, width=None, height=None, inter=cv2.INTER_AREA):
    """
    Resize image to specified dimensions.
    
    Args:
        image: Input image
        width: Target width (None to maintain aspect)
        height: Target height (None to maintain aspect)
        inter: Interpolation method
        
    Returns:
        Resized image
    """
    h, w = image.shape[:2]
    
    if width is None and height is None:
        return image
    
    if width is None:
        r = height / float(h)
        width = int(w * r)
    else:
        r = width / float(w)
        height = int(h * r)
    
    return cv2.resize(image, (width, height), interpolation=inter)


def draw_boxes(image, boxes, labels=None, color=(0, 255, 0), thickness=2):
    """
    Draw bounding boxes on image.
    
    Args:
        image: Input image
        boxes: List of [x1, y1, x2, y2] boxes
        labels: Optional labels for each box
        color: Box color (BGR)
        thickness: Line thickness
        
    Returns:
        Annotated image
    """
    img = image.copy()
    
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
        
        if labels:
            cv2.putText(img, str(labels[i]), (int(x1), int(y1) - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    return img


def calculate_centroid(box):
    """Calculate centroid of bounding box."""
    x1, y1, x2, y2 = box
    return np.array([(x1 + x2) / 2, (y1 + y2) / 2])


def iou(box1, box2):
    """
    Calculate Intersection over Union (IoU) between two boxes.
    
    Args:
        box1, box2: [x1, y1, x2, y2] format
        
    Returns:
        IoU score (0-1)
    """
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2
    
    # Calculate intersection
    inter_x_min = max(x1_min, x2_min)
    inter_y_min = max(y1_min, y2_min)
    inter_x_max = min(x1_max, x2_max)
    inter_y_max = min(y1_max, y2_max)
    
    if inter_x_max < inter_x_min or inter_y_max < inter_y_min:
        return 0.0
    
    inter_area = (inter_x_max - inter_x_min) * (inter_y_max - inter_y_min)
    
    # Calculate union
    box1_area = (x1_max - x1_min) * (y1_max - y1_min)
    box2_area = (x2_max - x2_min) * (y2_max - y2_min)
    union_area = box1_area + box2_area - inter_area
    
    if union_area == 0:
        return 0.0
    
    return inter_area / union_area


def get_video_properties(video_path):
    """Get video properties."""
    cap = cv2.VideoCapture(str(video_path))
    
    props = {
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    }
    
    cap.release()
    return props
