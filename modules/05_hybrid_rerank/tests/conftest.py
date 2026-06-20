import sys
from pathlib import Path

# Add the 05_hybrid_rerank directory to sys.path so its modules are directly importable
# (the directory name starts with a digit and can't be used as a dotted package path)
_modules = Path(__file__).parent.parent.parent
sys.path.insert(0, str(_modules / "05_hybrid_rerank"))
sys.path.insert(0, str(_modules / "04_semantic"))
sys.path.insert(0, str(_modules / "03_lexical"))
