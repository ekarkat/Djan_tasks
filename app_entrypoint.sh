#!/bin/sh

echo "Apply database migration and run server"

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

exec "$@"
