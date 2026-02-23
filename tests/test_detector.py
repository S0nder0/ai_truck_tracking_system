"""
Unit tests for truck detector module.
"""

import unittest
import numpy as np
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from truck_detector import TruckDetector, TruckTracker
from utils import calculate_centroid, iou


class TestTruckDetector(unittest.TestCase):
    """Test cases for TruckDetector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = TruckDetector(confidence_threshold=0.5)
    
    def test_detector_initialization(self):
        """Test detector initializes correctly."""
        self.assertEqual(self.detector.confidence_threshold, 0.5)
        self.assertIsNone(self.detector.model)
    
    def test_confidence_threshold(self):
        """Test confidence threshold is set correctly."""
        detector = TruckDetector(confidence_threshold=0.75)
        self.assertEqual(detector.confidence_threshold, 0.75)


class TestTruckTracker(unittest.TestCase):
    """Test cases for TruckTracker class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tracker = TruckTracker(max_disappeared=50)
    
    def test_tracker_initialization(self):
        """Test tracker initializes correctly."""
        self.assertEqual(self.tracker.max_disappeared, 50)
        self.assertEqual(self.tracker.next_id, 0)
        self.assertEqual(len(self.tracker.objects), 0)
    
    def test_tracker_update_empty(self):
        """Test tracker update with empty detections."""
        result = self.tracker.update([])
        self.assertEqual(len(result), 0)
    
    def test_tracker_update_single(self):
        """Test tracker update with single detection."""
        detection = {
            'centroid': np.array([100, 100]),
            'box': [50, 50, 150, 150],
            'confidence': 0.95
        }
        
        result = self.tracker.update([detection])
        self.assertEqual(len(result), 1)
        self.assertIn(0, result)


class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_calculate_centroid(self):
        """Test centroid calculation."""
        box = [0, 0, 100, 100]
        centroid = calculate_centroid(box)
        expected = np.array([50, 50])
        np.testing.assert_array_equal(centroid, expected)
    
    def test_iou_perfect_overlap(self):
        """Test IoU with perfect overlap."""
        box = [0, 0, 100, 100]
        result = iou(box, box)
        self.assertEqual(result, 1.0)
    
    def test_iou_no_overlap(self):
        """Test IoU with no overlap."""
        box1 = [0, 0, 100, 100]
        box2 = [200, 200, 300, 300]
        result = iou(box1, box2)
        self.assertEqual(result, 0.0)
    
    def test_iou_partial_overlap(self):
        """Test IoU with partial overlap."""
        box1 = [0, 0, 100, 100]
        box2 = [50, 50, 150, 150]
        result = iou(box1, box2)
        # Intersection = 50*50 = 2500
        # Union = 10000 + 10000 - 2500 = 17500
        # IoU = 2500 / 17500 ≈ 0.1429
        self.assertAlmostEqual(result, 0.1429, places=3)


if __name__ == '__main__':
    unittest.main()
