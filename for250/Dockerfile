FROM python:3.6

ENV DEPLOY_PATH /for250

RUN mkdir -p $DEPLOY_PATH
WORKDIR $DEPLOY_PATH

Add requirements.txt requirements.txt
RUN pip install -r requirements.txt

Add . .
