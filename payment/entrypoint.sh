#!/bin/bash

if [[ ! -d "src/modules/payment/migrations" ]]; then
    mkdir -p src/modules/payment/migrations
    touch src/modules/payment/migrations/__init__.py
fi

python src/bin/manage.py makemigrations
python src/bin/manage.py migrate

gunicorn src.config.wsgi:application --bind 0.0.0.0:8001