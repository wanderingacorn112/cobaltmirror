import requests, uuid, datetime
from db import SessionLocal
from models import RawArticle

class JSONFeedConnector:
    def __init__(self, url: str, feed_name: str):
        self.url = url
        self.feed_name = feed_name

    def run(self):
        response = requests.get(self.url)
        data = response.json()

        with SessionLocal() as db:
            for item in data["items"]:
                uid = uuid.uuid5(uuid.NAMESPACE_URL, item["url"])
                if db.get(RawArticle, uid):
                    continue
                rec = RawArticle(
                    id=uid,
                    title=item.get("title"),
                    summary=item.get("summary", ""),
                    content_html=item.get("content", ""),
                    url=item["url"],
                    published_at=datetime.datetime.fromisoformat(item["published_at"]),
                    collected_at=datetime.datetime.utcnow(),
                    source_type="json_api",
                    feed_name=self.feed_name,
                    reliability="C",  # adjust per source
                    raw_payload=item
                )
                db.add(rec)
            db.commit()
