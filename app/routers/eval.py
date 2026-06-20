from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter()


@router.get("/latest")
def get_latest_report():
    benchmark_dir = Path("data/benchmarks")
    if not benchmark_dir.exists():
        return {"error": "No benchmarks run yet"}
    reports = sorted(benchmark_dir.glob("*.json"), key=lambda p: p.stat().st_mtime)
    if not reports:
        return {"error": "No benchmark files found"}
    with open(reports[-1]) as f:
        return {"file": reports[-1].name, "report": json.load(f)}
