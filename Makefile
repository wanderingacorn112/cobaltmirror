# Makefile

.PHONY: up down init clean logs restart create-user

up:
	docker compose up -d

down:
	docker compose down

init:
	@echo "🔧 Initializing Airflow DB..."
	docker compose run --rm airflow-webserver airflow db init

create-user:
	@echo "👤 Creating Airflow admin user..."
	docker compose run --rm airflow-webserver airflow users create \
		--username admin --password admin \
		--firstname OSINT --lastname Admin \
		--role Admin --email admin@example.com

restart: down up

logs:
	docker compose logs -f --tail=100

clean:
	@echo "🧹 Removing containers and volumes..."
	docker compose down -v
	sudo rm -rf logs/ .airflow/
