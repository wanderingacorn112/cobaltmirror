from gnews import GNews
import uuid, datetime
from db import SessionLocal
from models import RawArticle

class GoogleNewsConnector:
    def __init__(self, query, feed_name):
        self.query = query
        self.feed_name = feed_name
        self.gnews = GNews(language='en', country='US')

    def run(self):
        results = self.gnews.get_news(self.query)
        with SessionLocal() as db:
            for item in results:
                uid = uuid.uuid5(uuid.NAMESPACE_URL, item["url"])
                if db.get(RawArticle, uid):
                    continue
                rec = RawArticle(
                    id=uid,
                    title=item.get("title"),
                    summary=item.get("description", ""),
                    content_html=item.get("description", ""),
                    url=item.get("url"),
                    published_at=item.get("published date"),
                    collected_at=datetime.datetime.utcnow(),
                    source_type="google_news",
                    feed_name=self.feed_name,
                    reliability="B",
                    raw_payload=item
                )
                db.add(rec)
            db.commit()
