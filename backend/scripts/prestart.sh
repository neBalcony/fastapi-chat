#!/bin/bash
set -e

echo "Initializing database..."
echo $(ls)
cd app

python backend_pre_start.py
echo "Database initialized."
echo
