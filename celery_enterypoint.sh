#!/bin/sh

celery -A djantasks worker --loglevel=info

exec "$@"
