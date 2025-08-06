#!/bin/bash

dir=$(dirname "$0")
python $dir/manage.py reset_db --no-input
python $dir/manage.py makemigrations
python $dir/manage.py migrate
python $dir/manage.py loaddata $dir/../data/initial_data.json

gunicorn src.config.wsgi:application --bind 0.0.0.0:8000