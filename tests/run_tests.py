"""
Run all tests for the truck tracking system.
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

if __name__ == '__main__':
    # Discover and run all tests
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
