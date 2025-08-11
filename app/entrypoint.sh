#!/bin/bash

python src/bin/manage.py migrate
python src/bin/manage.py loaddata src/data/initial.json 
python src/bin/manage.py loaddata src/data/providers.json 
python src/bin/manage.py collectstatic --noinput

gunicorn src.config.wsgi:application --bind 0.0.0.0:8000 --certfile=certs/cert.pem --keyfile=certs/key.pem