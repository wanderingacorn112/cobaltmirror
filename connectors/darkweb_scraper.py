import scrapy
import datetime, uuid
from scrapy.crawler import CrawlerProcess
from db import SessionLocal
from models import RawArticle

class OnionSpider(scrapy.Spider):
    name = "onion_spider"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 1,
        },
        "HTTPPROXY_ENABLED": True,
        "HTTPPROXY_AUTH_ENCODING": "utf-8",
        "DOWNLOAD_TIMEOUT": 30,
        "RETRY_TIMES": 3,
    }

    def __init__(self, start_url, feed_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.feed_name = feed_name
        self.proxy = "socks5h://localhost:9050"

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'proxy': self.proxy})

    def parse(self, response):
        title = response.xpath("//title/text()").get()
        content = response.xpath("//body//text()").getall()
        text = " ".join(content).strip()

        uid = uuid.uuid5(uuid.NAMESPACE_URL, response.url)
        with SessionLocal() as db:
            if db.get(RawArticle, uid):
                return
            db.add(RawArticle(
                id=uid,
                title=title,
                summary=text[:500],
                content_html=text,
                url=response.url,
                published_at=None,
                collected_at=datetime.datetime.utcnow(),
                source_type="darkweb",
                feed_name=self.feed_name,
                reliability="D",  # caution-tier source
                raw_payload=None
            ))
            db.commit()
from scrapy.crawler import CrawlerProcess
from connectors.darkweb_scraper import OnionSpider

def run_onion_scrape():
    process = CrawlerProcess()
    process.crawl(OnionSpider, start_url="http://someoniondomain.onion", feed_name="dark_forum_1")
    process.start()
