# dags/rss_ingest_to_pg.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from connectors.rss_pg import RSStoPostgres
from connectors.json_api_pg import JSONFeedConnector
from connectors.reddit_pg import RedditConnector
from airflow.operators.python import PythonOperator

PythonOperator(
    task_id="scrape_dark_forum",
    python_callable=run_onion_scrape
)


PythonOperator(
    task_id="pull_reddit_cybersec",
    python_callable=lambda: RedditConnector(
        client_id="your_id",
        client_secret="your_secret",
        user_agent="osint-ingestor",
        subreddit="cybersecurity",
        feed_name="reddit_cyber"
    ).run()
)


FEEDS = {
    "osint_conflict_api":
}

for name, url in FEEDS.items():
    PythonOperator(
        task_id=f"pull_{name}",
        python_callable=lambda url=url, name=name: JSONFeedConnector(url, name).run()
    )


FEEDS = {
    "reuters_world": "http://feeds.reuters.com/reuters/worldNews",
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "cnn_top": "http://rss.cnn.com/rss/edition.rss",
    "euronews": "https://www.euronews.com/rss?level=theme&name=news",
}

default_args = {
    "owner": "osint",
    "retries": 2,
    "retry_delay": timedelta(minutes=3),
}

def make_rss_task(url: str, feed_name: str):
    def task():
        RSStoPostgres(url, feed_name).run()
    return task

with DAG(
    dag_id="rss_ingest_to_pg",
    start_date=datetime(2025, 5, 29),
    schedule_interval="*/30 * * * *",
    catchup=False,
    default_args=default_args,
) as dag:
    for name, url in FEEDS.items():
        PythonOperator(
            task_id=f"pull_{name}",
            python_callable=make_rss_task(url, name),
        )
