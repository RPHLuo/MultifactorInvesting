FROM ubuntu:latest
FROM python:latest
WORKDIR /usr/src/app
COPY .. /usr/src/app
RUN apt-get update && apt-get install -y cron python-pip python-setuptools
RUN apt-get install -y libffi-dev libxml2-dev libxslt-dev lib32z1-dev libssl-dev
RUN pip3 install -r requirements.txt
