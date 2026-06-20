import sys
from pathlib import Path

# Add the 07_graph_filesystem directory to sys.path so its modules are directly importable
# (the directory name starts with a digit and can't be used as a dotted package path)
_root = Path(__file__).parent.parent.parent.parent  # project root
_modules = Path(__file__).parent.parent.parent      # modules/
sys.path.insert(0, str(_modules / "07_graph_filesystem"))
sys.path.insert(0, str(_root))  # so 'core' package is importable
