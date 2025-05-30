import praw
import uuid, datetime
from db import SessionLocal
from models import RawArticle

class RedditConnector:
    def __init__(self, client_id, client_secret, user_agent, subreddit, feed_name):
        self.subreddit = subreddit
        self.feed_name = feed_name
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )

    def run(self):
        with SessionLocal() as db:
            for post in self.reddit.subreddit(self.subreddit).hot(limit=50):
                uid = uuid.uuid5(uuid.NAMESPACE_URL, post.url)
                if db.get(RawArticle, uid):
                    continue
                rec = RawArticle(
                    id=uid,
                    title=post.title,
                    summary=post.selftext[:512],
                    content_html=post.selftext,
                    url=post.url,
                    published_at=datetime.datetime.fromtimestamp(post.created_utc),
                    collected_at=datetime.datetime.utcnow(),
                    source_type="reddit",
                    feed_name=self.feed_name,
                    reliability="C",
                    raw_payload=post.__dict__,
                )
                db.add(rec)
            db.commit()
