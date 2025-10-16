from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime
from database import SessionLocal, init_db
from models import Article
from scheduler import start_scheduler

app = FastAPI(title="CiberSec News Hub API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()
start_scheduler(app)

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}

@app.get("/articles")
def list_articles(
    q: Optional[str] = None,
    category: Optional[str] = None,
    severity: Optional[str] = None,
    source: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    db = SessionLocal()
    try:
        query = db.query(Article)
        if q:
            like = f"%{q.lower()}%"
            query = query.filter((Article.title.ilike(like)) | (Article.summary.ilike(like)))
        if category:
            query = query.filter(Article.category == category)
        if severity:
            query = query.filter(Article.severity == severity)
        if source:
            query = query.filter(Article.source == source)
        if date_from:
            query = query.filter(Article.published_at >= date_from)
        if date_to:
            query = query.filter(Article.published_at <= date_to)
        total = query.count()
        items = query.order_by(Article.published_at.desc()).offset(offset).limit(limit).all()
        return {"total": total, "items": [i.to_dict() for i in items]}
    finally:
        db.close()

@app.post("/ingest/run")
def run_ingestion():
    from ingest.rss_ingestor import run as run_rss
    count = run_rss()
    return {"ingested": count}
