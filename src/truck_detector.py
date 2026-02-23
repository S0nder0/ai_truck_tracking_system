"""
Truck Detection Module
Uses TensorFlow object detection to identify and track trucks in video/image feeds.
"""

import cv2
import numpy as np
import tensorflow as tf
from pathlib import Path


class TruckDetector:
    """Detects trucks in images and video streams using TensorFlow."""
    
    def __init__(self, model_path=None, confidence_threshold=0.5):
        """
        Initialize the truck detector.
        
        Args:
            model_path: Path to pre-trained model (optional)
            confidence_threshold: Minimum confidence for detection (0-1)
        """
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.model_path = model_path
        
        if model_path:
            self._load_model(model_path)
    
    def _load_model(self, model_path):
        """Load a saved TensorFlow model."""
        try:
            self.model = tf.saved_model.load(model_path)
            print(f"Model loaded from {model_path}")
        except Exception as e:
            print(f"Failed to load model: {e}")
            print("Using placeholder detection mode")
    
    def detect_in_image(self, image_path):
        """
        Detect trucks in a single image.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with detections and annotated image
        """
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        detections = self._perform_detection(image)
        
        # Draw bounding boxes
        annotated = self._draw_detections(image.copy(), detections)
        
        return {
            'detections': detections,
            'annotated_image': annotated,
            'original_image': image
        }
    
    def detect_in_video(self, video_path, output_path=None):
        """
        Detect trucks in video frames.
        
        Args:
            video_path: Path to video file
            output_path: Optional path to save annotated video
            
        Returns:
            List of frame detections
        """
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise ValueError(f"Could not open video: {video_path}")
        
        all_detections = []
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            detections = self._perform_detection(frame)
            all_detections.append({
                'frame': frame_count,
                'detections': detections
            })
            frame_count += 1
        
        cap.release()
        return all_detections
    
    def _perform_detection(self, image):
        """
        Perform object detection on image.
        In production, this would use a trained model.
        Currently uses placeholder logic for demonstration.
        """
        h, w = image.shape[:2]
        detections = []
        
        # Placeholder detection logic
        # In production, run image through trained model
        if self.model:
            # Use actual model inference here
            pass
        
        return detections
    
    def _draw_detections(self, image, detections):
        """Draw bounding boxes and labels on image."""
        for detection in detections:
            x1, y1, x2, y2 = detection['box']
            confidence = detection['confidence']
            label = detection['label']
            
            # Draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw label
            text = f"{label}: {confidence:.2f}"
            cv2.putText(image, text, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return image


class TruckTracker:
    """Tracks trucks across frames using centroid tracking."""
    
    def __init__(self, max_disappeared=50):
        """
        Initialize tracker.
        
        Args:
            max_disappeared: Frames to keep tracking before object is forgotten
        """
        self.max_disappeared = max_disappeared
        self.next_id = 0
        self.objects = {}
        self.disappeared = {}
    
    def update(self, detections):
        """
        Update tracked objects with new detections.
        
        Args:
            detections: List of current detections
            
        Returns:
            Dictionary of tracked objects with IDs
        """
        if len(detections) == 0:
            # Mark all objects as disappeared
            self.disappeared = {
                oid: self.disappeared.get(oid, 0) + 1
                for oid in list(self.objects.keys())
            }
            
            # Remove objects that disappeared too long
            for oid in list(self.disappeared.keys()):
                if self.disappeared[oid] > self.max_disappeared:
                    del self.objects[oid]
                    del self.disappeared[oid]
            
            return self.objects
        
        # Get centroids from detections
        centroids = np.array([d['centroid'] for d in detections])
        
        # Match new detections to tracked objects
        # Simple implementation - in production use Hungarian algorithm
        for centroid in centroids:
            if len(self.objects) == 0:
                self.objects[self.next_id] = centroid
                self.disappeared[self.next_id] = 0
                self.next_id += 1
            else:
                # Find closest existing object
                distances = [np.linalg.norm(centroid - c) for c in self.objects.values()]
                closest_id = min(self.objects.keys(), key=lambda k: distances[list(self.objects.keys()).index(k)])
                
                self.objects[closest_id] = centroid
                self.disappeared[closest_id] = 0
        
        return self.objects
