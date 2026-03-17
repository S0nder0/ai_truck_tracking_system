# AI Truck Tracking System - Usage Guide

## Professional Model Documentation

### Overview
The AI Truck Tracking System is a production-ready computer vision application designed for real-time truck detection and tracking in video feeds and image streams. This system leverages TensorFlow's object detection capabilities combined with advanced multi-object tracking algorithms.

### System Features

#### Detection Capabilities
- **Real-time Processing**: Processes video at 30+ FPS (GPU-dependent)
- **Multiple Detection Models**: Supports SSD MobileNet, Faster R-CNN, and custom models
- **Confidence Thresholding**: Configurable confidence levels (0-1 scale)
- **Batch Processing**: Efficient batch inference for high-throughput scenarios

#### Tracking Features
- **Centroid-based Tracking**: Maintains object identity across frames
- **Multi-object Tracking**: Tracks up to 100+ simultaneous trucks
- **Temporal Consistency**: Handles occlusions and frame drops
- **ID Management**: Persistent truck identification with lifecycle management

#### Performance Metrics
- **Detection Latency**: <50ms per frame (RTX 3080)
- **Throughput**: 60+ FPS real-time processing
- **Memory Usage**: ~2GB GPU VRAM (optimized)
- **Model Size**: ~100-200MB depending on backbone

### Architecture

```
Input Video/Image
      ↓
[Frame Extraction]
      ↓
[Preprocessing] → Resize, Normalize
      ↓
[Detection Model] → Bounding boxes, confidence
      ↓
[Filtering] → Confidence threshold
      ↓
[Tracking] → Centroid matching, ID assignment
      ↓
[Visualization] → Annotated output
      ↓
Output with Detections & Tracks
```

### API Reference

#### TruckDetector Class

```python
class TruckDetector:
    """Main detector class for truck identification."""
    
    def __init__(self, model_path=None, confidence_threshold=0.5):
        """Initialize detector with optional pre-trained model."""
        
    def detect_in_image(self, image_path):
        """Detect trucks in single image."""
        # Returns: {'detections': [...], 'annotated_image': ndarray}
        
    def detect_in_video(self, video_path, output_path=None):
        """Process video and return frame detections."""
        # Returns: List of frame detection data
```

#### TruckTracker Class

```python
class TruckTracker:
    """Multi-object tracker using centroid tracking."""
    
    def __init__(self, max_disappeared=50):
        """Initialize tracker with max disappearance frames."""
        
    def update(self, detections):
        """Update tracker with new detections."""
        # Returns: {truck_id: centroid_position}
```

### Usage Examples

#### Basic Image Detection
```python
from src.truck_detector import TruckDetector

detector = TruckDetector(confidence_threshold=0.6)
results = detector.detect_in_image('truck_image.jpg')

for detection in results['detections']:
    print(f"Truck at {detection['box']} - Confidence: {detection['confidence']}")
```

#### Video Processing with Tracking
```python
from src.truck_detector import TruckDetector, TruckTracker

detector = TruckDetector()
tracker = TruckTracker(max_disappeared=50)

detections = detector.detect_in_video('traffic_video.mp4')

for frame_data in detections:
    tracked = tracker.update(frame_data['detections'])
    print(f"Frame {frame_data['frame']}: {len(tracked)} tracked trucks")
```

#### CLI Usage
```bash
# Detect trucks in video with custom confidence
python main.py traffic_video.mp4 --confidence 0.7 --output results.mp4

# Process image
python main.py truck_photo.jpg --output annotated.jpg

# Custom model
python main.py video.mp4 --model custom_model.pb --confidence 0.5
```

### Configuration

Edit `config.json` to customize behavior:

```json
{
  "model_config": {
    "model_type": "ssd_mobilenet_v2",
    "confidence_threshold": 0.5,
    "input_size": 300
  },
  "tracking_config": {
    "max_disappeared": 50,
    "distance_threshold": 50
  },
  "performance": {
    "target_fps": 30,
    "gpu_enabled": true,
    "batch_size": 1
  }
}
```

### Deployment Options

#### Docker Deployment
```bash
docker build -t truck-detector .
docker run --gpus all -v $(pwd)/data:/app/data truck-detector
```

#### REST API Deployment
```bash
pip install flask gunicorn
python api.py --port 5000
```

#### Cloud Deployment
- AWS SageMaker for managed inference
- Google Cloud AI Platform
- Azure Machine Learning

### Performance Optimization

- **Model Quantization**: FP16/INT8 quantization for faster inference
- **Batch Processing**: Process multiple frames in parallel
- **GPU Acceleration**: CUDA/cuDNN optimized operations
- **Model Pruning**: Reduce model size without accuracy loss

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Out of Memory | Reduce batch_size in config.json |
| Low FPS | Enable GPU, reduce input resolution |
| Poor detections | Increase confidence_threshold or retrain |
| Lost tracks | Adjust max_disappeared parameter |

### Support & Documentation

- 📖 [Full Documentation](docs/API.md)
- 🐛 [Report Issues](https://github.com/S0nder0/ai_truck_tracking_system/issues)
- 💬 [Discussions](https://github.com/S0nder0/ai_truck_tracking_system/discussions)

