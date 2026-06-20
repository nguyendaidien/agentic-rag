import sys
from pathlib import Path

# Add the 04_semantic directory to sys.path so its modules are directly importable
# (the directory name starts with a digit and can't be used as a dotted package path)
sys.path.insert(0, str(Path(__file__).parent.parent))
