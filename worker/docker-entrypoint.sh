#!/usr/bin/env bash

echo "Running the worker configuration"

export PYTHONPATH=/home:$PYTHONPATH

celery -A app.main worker --loglevel=info