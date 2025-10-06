#!/bin/bash
set -e
ls
echo "[SCRIPT] RUN: backend_init_db.py"
python app/backend_init_db.py
echo "[SCRIPT] DONE"