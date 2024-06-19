#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python3 -m pip install -U --disable-pip-version-check .[non-termux]
python3 -m proxy_scraper_checker
cron
python ./proxy/manage.py migrate
python ./proxy/manage.py runserver 0:8000 # TODO : user gunicorn
#/usr/local/bin/gunicorn proxy.proxy.wsgi --bind 0.0.0.0:5000 --chdir=/app --worker-class=gevent --worker-connections=1000 --workers=3 --timeout 180