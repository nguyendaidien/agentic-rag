"""
Module 02: Generate synthetic golden set.
Usage: uv run python -m modules.02_evaluation.generate_golden_set
"""
from core.corpus import CorpusLoader
from evals.synthetic_data import build_golden_set

if __name__ == "__main__":
    loader = CorpusLoader()
    build_golden_set(loader, n=500)
