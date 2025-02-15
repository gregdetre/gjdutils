import os
import sys

# Add the root directory to Python path to import __VERSION__
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from __VERSION__ import __version__

# Export version at package level
__version__ = __version__
