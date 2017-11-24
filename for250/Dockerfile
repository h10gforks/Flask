FROM python:3.6

ENV DEPLOY_PATH /for250

RUN mkdir -p $DEPLOY_PATH
WORKDIR $DEPLOY_PATH

Add requirements.txt requirements.txt
Add manage.py manage.py
Add app app
RUN pip install -r requirements.txt
RUN python3 manage.py db init
RUN python3 manage.py db migrate
RUN python3 manage.py createdb

Add . .
