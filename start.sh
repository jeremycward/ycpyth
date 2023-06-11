#!/bin/bash
nohup redis-server &
gunicorn main:app --worker-class gevent --bind 0.0.0.0:5000