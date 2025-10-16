from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String(64), unique=True, index=True, nullable=False)
    title = Column(String(512), nullable=False)
    summary = Column(String(4000))
    url = Column(String(1024), nullable=False)
    source = Column(String(128), index=True)
    category = Column(String(64), index=True)
    risk_score = Column(Float, index=True)
    severity = Column(String(16), index=True)
    published_at = Column(DateTime, index=True)
    created_at = Column(DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "url": self.url,
            "source": self.source,
            "category": self.category,
            "risk_score": self.risk_score,
            "severity": self.severity,
            "published_at": self.published_at.isoformat() if self.published_at else None,
        }
