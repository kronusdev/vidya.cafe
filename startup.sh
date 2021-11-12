#!/bin/bash
if [ -n "$TMUX" ]; then
	pkill gunicorn
	cd /vidya.cafe
	sudo cp vidya.cafe/nginx.txt /etc/nginx/sites-available/vidya.cafe.conf
	sudo nginx -s reload
	. ./venv/bin/activate
	. ./env.sh
	cd /vidya.cafe/vidya.cafe
	pip install -r requirements.txt
	export PYTHONPATH=$PYTHONPATH:/vidya.cafe/vidya.cafe
	cd /vidya.cafe/vidya.cafe
	echo "starting regular workers"
	NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn files.__main__:app -k gevent -w $WEB_CONCURRENCY --max-requests 10000 --max-requests-jitter 500 --reload --bind 0.0.0.0:5000
else
	echo "Make sure to run the serevr inside tmux!"
	echo "Use 'tmux a' to attach to a running tmux session, or 'tmux' to start one. Then use 'tmux detach-client'"
fi
