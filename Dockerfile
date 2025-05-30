# Dockerfile

FROM apache/airflow:2.9.0-python3.11

USER root

# Install PostgreSQL driver and other optional providers
RUN pip install --no-cache-dir \
    psycopg2-binary \
    apache-airflow-providers-postgres \
    apache-airflow-providers-slack \
    apache-airflow-providers-http \
    apache-airflow-providers-amazon \
    apache-airflow-providers-docker \
    apache-airflow-providers-ftp

USER airflow
