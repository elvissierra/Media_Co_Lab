FROM python:3.10.0-slim as base

RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install psycopg2==2.9.9

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN mkdir -p /app/static

CMD ["gunicorn", "test_system.wsgi:application", "--bind", "0.0.0.0:8000"]

EXPOSE 8000
