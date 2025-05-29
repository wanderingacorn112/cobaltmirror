# dags/rss_ingest_to_pg.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from connectors.rss_pg import RSStoPostgres

FEEDS = {
    "reuters_world": "http://feeds.reuters.com/reuters/worldNews",
    "aljazeera_all": "https://www.aljazeera.com/xml/rss/all.xml",
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
