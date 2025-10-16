# backend/app.py
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, init_db
from models import Article
from scheduler import start_scheduler
from classifier import classify_category, CATEGORIES  # para reclassificar e listar categorias


app = FastAPI(title="CiberSec News Hub API", version="0.1.0")

# CORS liberado (front estático na Render)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# cria tabelas (se não existirem) e inicia o scheduler diário 07:00 BRT
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
    offset: int = Query(0, ge=0),
):
    db = SessionLocal()
    try:
        query = db.query(Article)
        if q:
            like = f"%{q.lower()}%"
            query = query.filter(
                (Article.title.ilike(like)) | (Article.summary.ilike(like))
            )
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
        items = (
            query.order_by(Article.published_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return {"total": total, "items": [i.to_dict() for i in items]}
    finally:
        db.close()


# -------- Ingestão em background --------
def _run_ingestion():
    from ingest.rss_ingestor import run as run_rss
    run_rss()

@app.post("/ingest/run")
def run_ingestion(background_tasks: BackgroundTasks):
    background_tasks.add_task(_run_ingestion)
    return {"status": "started"}


# -------- Reclassificação em massa --------
@app.post("/admin/reclassify")
def admin_reclassify():
    db = SessionLocal()
    updated = 0
    try:
        for art in db.query(Article).all():
            new_cat = classify_category(art.title or "", art.summary or "")
            if new_cat != art.category:
                art.category = new_cat
                updated += 1
        db.commit()
        return {"reclassified": updated}
    finally:
        db.close()


# -------- Listar categorias editoriais (para o front) --------
@app.get("/meta/categories")
def meta_categories():
    # expõe a lista de categorias definida no classifier.py
    return {"categories": CATEGORIES}

