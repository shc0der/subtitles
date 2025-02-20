#!/usr/bin/env bash

echo "Running the flower configuration"
celery -A app.main flower --port=5555