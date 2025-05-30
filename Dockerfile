# Use official Airflow base image
FROM apache/airflow:2.9.0-python3.11

USER airflow

# Install PostgreSQL driver and useful Airflow providers
RUN pip install --no-cache-dir \
    psycopg2-binary \
    apache-airflow-providers-postgres \
    apache-airflow-providers-slack \
    apache-airflow-providers-http \
    apache-airflow-providers-amazon \
    apache-airflow-providers-docker \
    apache-airflow-providers-ftp \
    feedparser \
    requests \
    pandas \
    sqlalchemy \
    tqdm

FROM python:3.11-slim
WORKDIR /app
COPY . /app
ENTRYPOINT ["cobaltmirror-enrich"]

# Optional: install NLP tools like spaCy later in enrichment container
# RUN pip install spacy

# Ensure Airflow user owns key folders
RUN mkdir -p /opt/airflow/logs /opt/airflow/dags /opt/airflow/plugins /opt/airflow/connectors && \
    chown -R airflow: /opt/airflow

USER airflow
