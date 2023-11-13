import sys
from pathlib import Path

# Adjust the path so tests can import the src modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
