#!/bin/bash
# scripts/bootstrap.sh

set -e

echo "🌐 Generating Fernet key..."
FERNET_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")

cat <<EOF > .env
POSTGRES_USER=osint
POSTGRES_PASSWORD=super-secret
POSTGRES_DB=osint
AIRFLOW__CORE__FERNET_KEY=$FERNET_KEY
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://osint:super-secret@postgres:5432/osint
EOF

echo "✅ .env created."

echo "🧼 Fixing log permissions..."
sudo rm -rf logs/
mkdir -p logs/
sudo chmod -R 777 logs/

echo "📦 Building and starting containers..."
sudo docker compose build
sudo docker compose up -d

echo "📚 Initializing Airflow DB and user..."
sudo docker compose run --rm airflow-webserver airflow db init
sudo docker compose run --rm airflow-webserver airflow users create \
	--username admin --password admin \
	--firstname OSINT --lastname Admin \
	--role Admin --email admin@example.com

echo "✅ Setup complete. Visit http://localhost:8080 (admin/admin)"
