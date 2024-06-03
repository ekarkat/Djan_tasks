#!/bin/sh

celery -A djantasks worker --loglevel=info
celery -A djantasks beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler

exec "$@"
