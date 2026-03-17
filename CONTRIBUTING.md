# Contributing to AI Truck Tracking System

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

### Our Commitment
We are committed to providing a welcoming and inspiring community for all. Please be respectful, inclusive, and professional.

### Standards
- Use welcoming and inclusive language
- Be respectful of differing opinions and experiences
- Gracefully accept constructive criticism
- Focus on what's best for the community

## Getting Started

### Prerequisites
- Python 3.8+
- Git
- Virtual environment setup
- TensorFlow 2.10+

### Development Setup

1. **Fork the repository**
```bash
# Visit https://github.com/S0nder0/ai_truck_tracking_system
# Click "Fork"
```

2. **Clone your fork**
```bash
git clone https://github.com/YOUR_USERNAME/ai_truck_tracking_system.git
cd ai_truck_tracking_system
```

3. **Create development branch**
```bash
git checkout -b feature/your-feature-name
```

4. **Setup environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

## Development Guidelines

### Code Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable names
- Add docstrings to all functions and classes
- Keep functions small and focused (< 100 lines)

### Testing Requirements
- Write unit tests for new features
- Maintain >80% code coverage
- Run tests before submitting PR

```bash
pytest tests/
pytest --cov=src tests/  # With coverage
```

### Commit Messages
Use clear, descriptive commit messages:

```
# Good
feat: add centroid tracking for multi-object detection
fix: resolve memory leak in video processing
docs: update installation instructions

# Avoid
update code
fix bug
changes
```

### Documentation
- Update README.md for user-facing changes
- Add docstrings to new functions
- Update USAGE_GUIDE.md for feature changes
- Include examples for new functionality

## Types of Contributions

### Bug Reports
- Use GitHub Issues
- Include:
  - Python version and OS
  - TensorFlow version
  - Minimal reproduction code
  - Error traceback
  - Expected vs actual behavior

### Feature Requests
- Describe the feature clearly
- Explain the use case
- Provide examples
- Discuss implementation approach

### Code Contributions
- Submit PRs with clear descriptions
- Reference issues being fixed
- Include tests
- Update documentation
- Keep PRs focused (one feature per PR)

## Pull Request Process

### Before Submitting
1. ✅ Tests pass: `pytest tests/`
2. ✅ Code style: `pylint src/`
3. ✅ No security issues
4. ✅ Documentation updated
5. ✅ CHANGELOG updated

### Submission
1. Push to your fork
2. Create Pull Request with clear title
3. Fill PR template completely
4. Link related issues
5. Request review

### PR Title Format
- `feat: Brief description`
- `fix: Brief description`
- `docs: Brief description`
- `refactor: Brief description`
- `test: Brief description`

### Review Process
- Maintainers will review within 48 hours
- Address feedback and update PR
- Squash commits if requested
- Merge when approved

## Development Workflow

### Feature Development
```bash
git checkout -b feature/new-feature
# Make changes
pytest tests/
git commit -m "feat: add new feature"
git push origin feature/new-feature
# Create Pull Request
```

### Bug Fix
```bash
git checkout -b fix/bug-name
# Fix the bug
pytest tests/
git commit -m "fix: resolve issue with X"
git push origin fix/bug-name
# Create Pull Request
```

## Project Structure

```
ai_truck_tracking_system/
├── src/
│   ├── __init__.py
│   ├── truck_detector.py
│   ├── utils.py
│   └── tracking.py
├── tests/
│   ├── test_detector.py
│   ├── test_tracking.py
│   └── test_utils.py
├── docs/
│   ├── API.md
│   └── DEPLOYMENT.md
├── examples/
│   └── basic_usage.py
└── CONTRIBUTING.md
```

## Coding Standards

### Type Hints
```python
def process_image(image_path: str) -> Dict[str, Any]:
    """Process image and return detections."""
```

### Docstring Format
```python
def detect_trucks(self, video_path: str) -> List[Dict]:
    """
    Detect trucks in video.
    
    Args:
        video_path: Path to video file
        
    Returns:
        List of frame detections with format:
        [{'frame': int, 'detections': List[Dict]}]
        
    Raises:
        FileNotFoundError: If video file not found
        ValueError: If video format not supported
    """
```

### Error Handling
```python
try:
    model = load_model(model_path)
except FileNotFoundError:
    logger.error(f"Model not found: {model_path}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

## Testing Guidelines

### Test Organization
```python
class TestTruckDetector:
    """Tests for TruckDetector class."""
    
    def setup_method(self):
        """Setup before each test."""
        
    def test_detector_initialization(self):
        """Test detector initializes correctly."""
        
    def teardown_method(self):
        """Cleanup after each test."""
```

### Mocking External Dependencies
```python
from unittest.mock import Mock, patch

def test_inference():
    with patch('tensorflow.saved_model.load') as mock_load:
        mock_load.return_value = Mock()
        detector = TruckDetector(confidence_threshold=0.5)
        assert detector is not None
```

## Performance Considerations

- Profile code to identify bottlenecks
- Use vectorized operations (NumPy)
- Minimize memory allocations in loops
- Cache expensive computations
- Document performance characteristics

## Documentation Standards

- Keep documentation up-to-date
- Include code examples
- Explain complex algorithms
- Link related concepts
- Update CHANGELOG.md

## Maintenance

The maintainers are responsible for:
- Reviewing and merging PRs
- Releasing new versions
- Maintaining dependencies
- Security updates
- Community engagement

## Resources

- 📚 [TensorFlow Documentation](https://www.tensorflow.org/api_docs)
- 📚 [OpenCV Documentation](https://docs.opencv.org/)
- 🧪 [Pytest Documentation](https://docs.pytest.org/)
- 📖 [Python Style Guide](https://www.python.org/dev/peps/pep-0008/)

## Questions?

- 💬 [GitHub Discussions](https://github.com/S0nder0/ai_truck_tracking_system/discussions)
- 🐛 [GitHub Issues](https://github.com/S0nder0/ai_truck_tracking_system/issues)
- 📧 Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

**Thank you for contributing to make this project better! 🚀**

