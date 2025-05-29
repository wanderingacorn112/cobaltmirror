# connectors/rss_pg.py
import hashlib
import uuid
import datetime
import feedparser
import logging

from db import SessionLocal
from models import RawArticle

log = logging.getLogger("rss_pg")

class RSStoPostgres:
    def __init__(self, url: str, feed_name: str):
        self.url = url
        self.feed_name = feed_name

    def run(self):
        feed = feedparser.parse(self.url)
        with SessionLocal() as db:
            for entry in feed.entries:
                uid = uuid.UUID(hashlib.md5(entry.link.encode()).hexdigest())
                if db.get(RawArticle, uid):
                    continue
                content = entry.get("content", [{"value": entry.get("summary", "")}])[0]["value"]
                rec = RawArticle(
                    id=uid,
                    title=entry.title,
                    summary=entry.get("summary", ""),
                    content_html=content,
                    url=entry.link,
                    source_type="rss",
                    feed_name=self.feed_name,
                    reliability="B",
                    collected_at=datetime.datetime.utcnow(),
                    published_at=datetime.datetime(*entry.published_parsed[:6]) if entry.get("published_parsed") else None,
                    raw_payload=dict(entry)
                )
                db.add(rec)
            db.commit()
