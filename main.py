"""
Main entry point for AI Truck Tracking System.
"""

import argparse
from pathlib import Path
from src.truck_detector import TruckDetector, TruckTracker
from src.utils import save_image, get_video_properties


def main():
    parser = argparse.ArgumentParser(
        description='AI Truck Tracking System - Detect and track trucks in videos/images'
    )
    
    parser.add_argument('input', help='Path to input image or video')
    parser.add_argument('--output', help='Path to save output (optional)')
    parser.add_argument('--model', help='Path to custom model (optional)')
    parser.add_argument('--confidence', type=float, default=0.5,
                       help='Confidence threshold (0-1)')
    parser.add_argument('--max-disappeared', type=int, default=50,
                       help='Max frames to track before forgetting object')
    
    args = parser.parse_args()
    
    # Validate input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}")
        return 1
    
    # Initialize detector and tracker
    detector = TruckDetector(model_path=args.model, 
                            confidence_threshold=args.confidence)
    tracker = TruckTracker(max_disappeared=args.max_disappeared)
    
    print(f"Confidence threshold: {args.confidence}")
    print(f"Max disappeared frames: {args.max_disappeared}")
    
    # Process input
    if input_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
        # Image processing
        print(f"Processing image: {input_path}")
        try:
            results = detector.detect_in_image(str(input_path))
            detections = results['detections']
            annotated = results['annotated_image']
            
            print(f"Found {len(detections)} trucks")
            
            # Save output if specified
            if args.output:
                output_path = Path(args.output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                save_image(annotated, str(output_path))
                print(f"Saved output to: {output_path}")
                
        except Exception as e:
            print(f"Error processing image: {e}")
            return 1
    
    elif input_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
        # Video processing
        print(f"Processing video: {input_path}")
        try:
            # Get video info
            props = get_video_properties(str(input_path))
            print(f"Video properties: {props}")
            
            # Detect trucks in video
            detections = detector.detect_in_video(str(input_path))
            
            print(f"Processed {len(detections)} frames")
            
            # Print summary
            total_trucks = sum(len(d['detections']) for d in detections)
            print(f"Total trucks detected: {total_trucks}")
            
            # Print per-frame info
            for frame_data in detections[:5]:  # Show first 5 frames
                frame_num = frame_data['frame']
                truck_count = len(frame_data['detections'])
                if truck_count > 0:
                    print(f"  Frame {frame_num}: {truck_count} trucks")
            
        except Exception as e:
            print(f"Error processing video: {e}")
            return 1
    
    else:
        print(f"Error: Unsupported file format: {input_path.suffix}")
        return 1
    
    print("Processing complete!")
    return 0


if __name__ == '__main__':
    exit(main())
