FROM python:3.12-slim

# базовые утилиты
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev python3-dev \
 && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip setuptools wheel

WORKDIR /app/

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./scripts ./scripts 
COPY ./alembic.ini ./alembic.ini

COPY ./app ./app

EXPOSE ${PORT:-8000}

CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
