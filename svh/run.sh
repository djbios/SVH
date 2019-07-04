#!/bin/bash

trap 'exit' ERR
python manage.py migrate --fake-initial --noinput

exec /usr/local/bin/uwsgi \
    --socket=uwsgi:9000 \
    --chdir=/www/svh/ \
    --uid=www-data \
    --gid=www-data \
    --wsgi-file=/www/svh/svh/wsgi.py \
    --module=wsgi \
    --auto-procname \
    --processes=3 \
    --master \
    --die-on-term \
    --vacuum
