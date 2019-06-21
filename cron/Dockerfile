FROM ubuntu:latest
FROM python:latest
WORKDIR /usr/src/app
COPY . /usr/src/app
ADD crontab /etc/cron.d/scrape
RUN chmod 0644 /etc/cron.d/scrape
RUN touch /var/log/cron.log
RUN apt-get update && apt-get install -y cron python-pip python-setuptools
RUN apt-get install -y libffi-dev libxml2-dev libxslt-dev lib32z1-dev libssl-dev
RUN pip3 install -r requirements.txt
CMD ["cron", "-f"]
