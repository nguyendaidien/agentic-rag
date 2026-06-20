from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import search, eval as eval_router

app = FastAPI(title="Agentic RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(eval_router.router, prefix="/eval", tags=["eval"])


@app.get("/health")
def health():
    return {"status": "ok"}
