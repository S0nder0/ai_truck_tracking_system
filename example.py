"""
Example usage of AI Truck Tracking System.
"""

from src.truck_detector import TruckDetector, TruckTracker
from pathlib import Path


def example_image_detection():
    """Example: Detect trucks in a single image."""
    print("=== Image Detection Example ===\n")
    
    detector = TruckDetector(confidence_threshold=0.5)
    
    # Example image path (replace with actual path)
    image_path = 'data/sample_image.jpg'
    
    if not Path(image_path).exists():
        print(f"Note: Sample image not found at {image_path}")
        print("To test, add an image file there.")
        return
    
    try:
        results = detector.detect_in_image(image_path)
        detections = results['detections']
        annotated_image = results['annotated_image']
        
        print(f"Detections found: {len(detections)}")
        for i, detection in enumerate(detections):
            print(f"  Truck {i+1}: {detection}")
        
        # Save annotated image
        from src.utils import save_image
        output_path = 'results/annotated_image.jpg'
        Path('results').mkdir(exist_ok=True)
        save_image(annotated_image, output_path)
        print(f"Annotated image saved to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")


def example_video_detection():
    """Example: Detect trucks in video."""
    print("\n=== Video Detection Example ===\n")
    
    detector = TruckDetector(confidence_threshold=0.5)
    tracker = TruckTracker(max_disappeared=50)
    
    # Example video path
    video_path = 'data/sample_video.mp4'
    
    if not Path(video_path).exists():
        print(f"Note: Sample video not found at {video_path}")
        print("To test, add a video file there.")
        return
    
    try:
        detections = detector.detect_in_video(video_path)
        
        print(f"Processed {len(detections)} frames")
        
        # Show detections from first few frames
        for frame_data in detections[:10]:
            frame_num = frame_data['frame']
            trucks = frame_data['detections']
            
            if len(trucks) > 0:
                # Update tracker
                tracked = tracker.update(trucks)
                print(f"Frame {frame_num}: {len(trucks)} trucks, {len(tracked)} tracked IDs")
        
    except Exception as e:
        print(f"Error: {e}")


def example_tracking():
    """Example: Basic tracking functionality."""
    print("\n=== Tracking Example ===\n")
    
    tracker = TruckTracker(max_disappeared=50)
    
    # Simulate detections across frames
    import numpy as np
    
    # Frame 1: Two trucks
    detections_frame1 = [
        {'centroid': np.array([100.0, 100.0]), 'box': [50, 50, 150, 150], 'confidence': 0.95},
        {'centroid': np.array([300.0, 300.0]), 'box': [250, 250, 350, 350], 'confidence': 0.92},
    ]
    
    tracked = tracker.update(detections_frame1)
    print(f"Frame 1: Tracked {len(tracked)} objects")
    for obj_id, centroid in tracked.items():
        print(f"  Truck {obj_id}: position {centroid}")
    
    # Frame 2: Same trucks moved
    detections_frame2 = [
        {'centroid': np.array([105.0, 105.0]), 'box': [55, 55, 155, 155], 'confidence': 0.93},
        {'centroid': np.array([305.0, 305.0]), 'box': [255, 255, 355, 355], 'confidence': 0.91},
    ]
    
    tracked = tracker.update(detections_frame2)
    print(f"\nFrame 2: Tracked {len(tracked)} objects")
    for obj_id, centroid in tracked.items():
        print(f"  Truck {obj_id}: position {centroid}")


if __name__ == '__main__':
    print("AI Truck Tracking System - Examples\n")
    print("=" * 50)
    
    example_image_detection()
    example_video_detection()
    example_tracking()
    
    print("\n" + "=" * 50)
    print("Examples complete!")
    print("\nNext steps:")
    print("1. Replace sample data with real images/videos")
    print("2. Train or download a pre-trained truck detection model")
    print("3. Configure model path in truck_detector.py")
    print("4. Run: python main.py <input_file> --output <output_file>")
