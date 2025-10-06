#!/bin/bash
set -e
ls
echo "[SCRIPT] RUN: backend_pre_start.py"
python app/backend_pre_start.py
echo "[SCRIPT] RUN: alembic upgrade head"
alembic upgrade head
echo "[SCRIPT] DONE"