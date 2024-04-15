#Python version
FROM python:3.10.0-alpine as base

#App structure- in order to mirror app structure and locate entry and manage deps
WORKDIR /app

#Deps- requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

#Env vars- app specifics
ENV DEBUG=False

#Static and media- how these are to be handled
RUN python manage.py collectstatic --noinput

#WSGI server like Gunicorn

#Port exposing

#CMD or Entry Point- how to run app once started
