FROM ubuntu
FROM python
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN apt-get update && apt-get install -y python-pip python-setuptools
RUN apt-get install -y libffi-dev libxml2-dev libxslt-dev lib32z1-dev libssl-dev
RUN pip install scrapy
RUN pip install pymongo
RUN pip install scrapy-splash
CMD ["scrapy","runspider","./updateStockData.py"]
