#!/bin/bash
/usr/local/bin/scrapy runspider ./scraper/updateStockData.py
python ./updateNeural.py
date
