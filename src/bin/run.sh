#!/bin/bash

dir=$(dirname "$0")
python $dir/manage.py migrate
python $dir/manage.py loaddata $dir/../data/initial_data.json

#gunicorn src.config.wsgi:application --bind 0.0.0.0:8000
python $dir/manage.py runserver 0.0.0.0:8000