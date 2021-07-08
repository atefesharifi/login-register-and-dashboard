# syntax=docker/dockerfile:1
FROM ${DOCKER_REGISTERY_PATH}python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /facecup
COPY requirements.txt /facecup/
RUN pip install -r requirements.txt
RUN pip install psycopg2
COPY . /facecup/
CMD python /facecup/manage.py makemigrations && python /facecup/manage.py migrate && python /facecup/manage.py runserver 0.0.0.0:${FACECUP_PORT}