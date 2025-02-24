#!/usr/bin/env bash

echo "Running the frontend configuration"

export PYTHONPATH=/home:$PYTHONPATH

python app/main.py