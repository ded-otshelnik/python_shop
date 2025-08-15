#!/bin/bash

python src/bin/manage.py migrate

gunicorn src.config.wsgi:application --bind 0.0.0.0:8001 --certfile=certs/cert.pem --keyfile=certs/key.pem