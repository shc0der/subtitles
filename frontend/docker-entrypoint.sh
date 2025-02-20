#!/usr/bin/env bash

echo "Running the frontend configuration"

export PYTHONPATH=/home:$PYTHONPATH

streamlit run app/main.py --server.port 8080 --server.maxUploadSize 250