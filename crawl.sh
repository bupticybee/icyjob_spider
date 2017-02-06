#!/bin/bash 
cd /alidata/workspace/icyjobscrapy/jobspy
/usr/local/bin/scrapy crawlall  > access.log 2>&1

echo "ddd" >> crontab.out
