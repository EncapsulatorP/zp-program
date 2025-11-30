import pathlib
import sys

# Ensure the project root is on sys.path so test modules can import z_p.*
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
