#!/bin/bash
/usr/local/bin/scrapy runspider ./scraper/updateStockData.py
python ./maintainData.py
python ./updateNeural.py
python ./runNeural.py
date
