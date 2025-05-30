#!/bin/bash

case "$1" in
  up)
    sudo docker compose up -d
    ;;
  down)
    sudo docker compose down
    ;;
  init)
    sudo docker compose run --rm airflow-webserver airflow db init
    ;;
  create-user)
    sudo docker compose run --rm airflow-webserver airflow users create \
      --username admin --password admin \
      --firstname OSINT --lastname Admin \
      --role Admin --email admin@example.com
    ;;
  rebuild)
    sudo docker compose down -v
    sudo docker compose build
    sudo docker compose up -d
    ;;
  clean)
    sudo docker compose down -v
    sudo rm -rf logs/ .airflow/ __pycache__/
    ;;
  logs)
    sudo docker compose logs -f --tail=100
    ;;
  *)
    echo "Usage: $0 {up|down|init|create-user|rebuild|clean|logs}"
    exit 1
    ;;
esac
