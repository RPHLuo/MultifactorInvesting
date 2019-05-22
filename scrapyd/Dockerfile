FROM ubuntu

RUN apt-get update && apt-get install -y \
			python-dev python-pip python-setuptools \
			libffi-dev libxml2-dev libxslt1-dev \
			libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev \
			liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk

RUN apt-get install scrapyd
RUN pip install scrapy
RUN pip install pymongo
RUN pip install scrapy-splash
RUN mkdir /etc/scrapyd/
RUN echo "[scrapyd] \n bind_address = 0.0.0.0" > /etc/scrapyd/scrapyd.conf

EXPOSE 6800
VOLUME ["/var/lib/scrapyd"]
CMD ["scrapyd &"]

