FROM python:3.5

RUN pip install scrapyd
RUN pip install dateparser
RUN mkdir /etc/scrapyd/
RUN echo "[scrapyd] \n bind_address = 0.0.0.0" > /etc/scrapyd/scrapyd.conf

EXPOSE 6800
CMD ["scrapyd"]
