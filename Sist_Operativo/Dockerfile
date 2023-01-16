# importing base image
FROM python:3.11.0-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requeriments.txt .
RUN pip install -r requeriments.txt
COPY . .
CMD python manage.py runserver --insecure 0.0.0.0:80