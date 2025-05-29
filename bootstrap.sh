#!/bin/bash
# scripts/bootstrap.sh

set -e

echo "🌐 Generating Fernet key..."
FERNET_KEY=$(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")

cat <<EOF > .env
# PostgreSQL
POSTGRES_USER=osint
POSTGRES_PASSWORD=super-secret
POSTGRES_DB=osint

# Airflow
AIRFLOW__CORE__FERNET_KEY=$FERNET_KEY
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg://osint:super-secret@postgres:5432/osint
EOF

echo "✅ .env created with fresh Fernet key."

echo "📦 Installing Python dependencies (optional local venv)..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

echo "✅ Bootstrap complete. Now run:"
echo "   make up && make init && make create-user"
