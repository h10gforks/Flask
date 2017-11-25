FROM python:2.7

ENV DEPLOY_PATH /for250

RUN mkdir -p $DEPLOY_PATH
WORKDIR $DEPLOY_PATH

COPY requirements.txt requirements.txt
COPY manage.py manage.py
COPY app app
COPY config.py config.py

RUN pip install -r requirements.txt
RUN python manage.py db init
RUN python manage.py db migrate
RUN python manage.py createdb

Add . .
