#!/bin/bash

if [[ ! -d "src/modules/web/migrations" ]]; then
    mkdir -p src/modules/web/migrations
    touch src/modules/web/migrations/__init__.py
fi

if [[ ! -d "src/modules/authetication/migrations" ]]; then
    mkdir -p src/modules/authetication/migrations
    touch src/modules/authetication/migrations/__init__.py
fi


python src/bin/manage.py makemigrations
python src/bin/manage.py migrate
python src/bin/manage.py loaddata src/data/initial.json
python src/bin/manage.py loaddata src/data/providers.json
python src/bin/manage.py collectstatic --noinput

gunicorn src.config.wsgi:application --bind 0.0.0.0:8000