from telethon.sync import TelegramClient
import uuid, datetime
from db import SessionLocal
from models import RawArticle

class TelegramConnector:
    def __init__(self, api_id, api_hash, channel, feed_name):
        self.api_id = api_id
        self.api_hash = api_hash
        self.channel = channel
        self.feed_name = feed_name

    def run(self):
        with TelegramClient("osint_session", self.api_id, self.api_hash) as client:
            messages = client.iter_messages(self.channel, limit=50)
            with SessionLocal() as db:
                for msg in messages:
                    if not msg.message:
                        continue
                    uid = uuid.uuid5(uuid.NAMESPACE_OID, str(msg.id))
                    if db.get(RawArticle, uid):
                        continue
                    rec = RawArticle(
                        id=uid,
                        title=None,
                        summary=msg.message[:512],
                        content_html=msg.message,
                        url=f"https://t.me/{self.channel}/{msg.id}",
                        published_at=msg.date,
                        collected_at=datetime.datetime.utcnow(),
                        source_type="telegram",
                        feed_name=self.feed_name,
                        reliability="C",
                        raw_payload=msg.to_dict()
                    )
                    db.add(rec)
                db.commit()
