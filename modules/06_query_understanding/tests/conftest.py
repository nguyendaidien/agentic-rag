import sys
from pathlib import Path

# Add the 06_query_understanding directory to sys.path so its modules are directly importable
# (the directory name starts with a digit and can't be used as a dotted package path)
_modules = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_modules / "06_query_understanding"))
