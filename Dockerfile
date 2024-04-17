#Python version
FROM python:3.10.0-alpine as base

#Install necessary packages
RUN apk add --update --no-cache --virtual .tmp-build-deps 

RUN apk add --no-cache libpq=15.6-r0


#App structure- in order to mirror app structure and locate entry and manage deps
WORKDIR /app

#Upgrade pip
RUN pip install --upgrade --no-cache-dir pip==24.0.0

#Deps- requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

#clean up temp depsCOPY . /app
RUN apk del .tmp-build-deps

#Env vars- app specifics
ENV DEBUG=False

#Static and media- how these are to be handled
RUN python manage.py collectstatic --noinput

#WSGI server like Gunicorn

#Port exposing

#CMD or Entry Point- how to run app once started
EXPOSE 8000
CMD [""]