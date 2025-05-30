# Dockerfile  – builds the Airflow runtime with project deps baked in
FROM apache/airflow:2.9.0-python3.11

# Install Python dependencies for the whole stack
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy source so scheduler + webserver both see DAGs & connectors
COPY . /opt/airflow
ENV PYTHONPATH="/opt/airflow"
