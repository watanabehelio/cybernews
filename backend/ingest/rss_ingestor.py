import yaml, feedparser, hashlib
from datetime import datetime
from pathlib import Path
from database import SessionLocal
from models import Article
from classifier import classify_category
from risk import score_and_severity

BASE = Path(__file__).resolve().parent
SOURCES = BASE / "sources.yaml"

def canonical_id(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()

def run() -> int:
    with open(SOURCES, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    sources = cfg.get("sources", [])

    db = SessionLocal()
    ingested = 0
    try:
        for s in sources:
            if s.get("type") != "rss":
                continue
            feed = feedparser.parse(s["url"])
            for e in feed.entries:
                link = e.get("link")
                if not link:
                    continue
                uid = canonical_id(link)
                if db.query(Article).filter(Article.uid == uid).first():
                    continue
                title = (e.get("title") or "").strip()
                summary = (e.get("summary") or e.get("description") or "").strip()
                published = e.get("published") or e.get("updated")
                published_at = None
                if published and getattr(e, "published_parsed", None):
                    try:
                        published_at = datetime(*e.published_parsed[:6])
                    except Exception:
                        published_at = datetime.utcnow()
                else:
                    published_at = datetime.utcnow()

                category = classify_category(title, summary)
                risk_score, severity = score_and_severity(title, summary)

                art = Article(
                    uid=uid,
                    title=title[:512],
                    summary=summary[:4000],
                    url=link,
                    source=s["name"],
                    category=category,
                    risk_score=risk_score,
                    severity=severity,
                    published_at=published_at,
                    created_at=datetime.utcnow(),
                )
                db.add(art)
                ingested += 1
        db.commit()
    finally:
        db.close()
    return ingested
