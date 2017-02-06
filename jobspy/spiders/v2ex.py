# -*- coding: utf-8 -*-
import scrapy
from jobspy.modules.mail import get_mail
from jobspy.modules.jobbean import *
from scrapy.http import Request
from jobspy.items import JobItem
from scrapy.utils.url import urljoin_rfc
import time
from datetime import timedelta
from datetime import datetime
import traceback


class V2EXSpider(scrapy.Spider):
    name = "v2exintern"
    allowed_domains = ["www.v2ex.com"]
    start_urls = [
        "http://www.v2ex.com/go/jobs?p=1",
        "http://www.v2ex.com/go/jobs?p=2",
        
    ]


    def start_requests(self):  

        for url in self.start_urls:
            
            yield Request(  
                url, headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, sdch',
		        'Accept-Language':'zh-CN,zh;q=0.8',
                #'Cache-Control':'max-age=0',
                'Connection':'keep-alive',
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36",
		      'Upgrade-Insecure-Requests':1,
                'Host': "www.v2ex.com",
                'Referer':'http://www.v2ex.com',
                'If-None-Match':'W/"da5030c23f460216165f7aee7fc37d318eeeb8de"',
                },

                cookies = {
                    'V2EX_TAB':"2|1:0|10:1462865435|8:V2EX_TAB|8:am9icw==|31cff524fccbec833661a4337772681c48570895ae491441c5b24cc5835d6f03",
                    'V2EX_LANG':'zhcn',
                    'PB3_SESSION':"2|1:0|10:1463317994|11:PB3_SESSION|36:djJleDo2MS40OS42Mi4xMDA6ODg2NjcyNTc=|cd3790b4828b836a238021307c74b051af453c6098132370fec735b73df127dd",
                    'A2':"2|1:0|10:1462193774|2:A2|56:Y2E3M2E1NzEyNDcyNTdmOTZkYmI2NmU4MjQ0Yjc4ODRjNTgwODkwYg==|269bb7c54207090d537b4f11ab2169f7fdb29dec24d7d1cc55091909bdc968b0",
                    '_gat':1,
                    '_ga': "GA1.2.667794905.1462193835"
                }

                )


    def parse(self, response):
        articles = response.xpath("//div[@id='TopicsNode']//div/table//span[@class='item_title']/a")
        for article in articles:
            try:
                article_link = article.xpath('@href').extract()[0]
                article_url = urljoin_rfc('http://www.v2ex.com/', article_link)
                # manage duplicate url
                if [i for i in JobModel.where(url=article_url).select()]:
                    return
                yield Request(url=article_url, callback=self.parse_article,cookies = {
                    'V2EX_TAB':"2|1:0|10:1462865435|8:V2EX_TAB|8:am9icw==|31cff524fccbec833661a4337772681c48570895ae491441c5b24cc5835d6f03",
                    'V2EX_LANG':'zhcn',
                    'PB3_SESSION':"2|1:0|10:1463317994|11:PB3_SESSION|36:djJleDo2MS40OS42Mi4xMDA6ODg2NjcyNTc=|cd3790b4828b836a238021307c74b051af453c6098132370fec735b73df127dd",
                    'A2':"2|1:0|10:1462193774|2:A2|56:Y2E3M2E1NzEyNDcyNTdmOTZkYmI2NmU4MjQ0Yjc4ODRjNTgwODkwYg==|269bb7c54207090d537b4f11ab2169f7fdb29dec24d7d1cc55091909bdc968b0",
                    '_gat':1,
                    '_ga': "GA1.2.667794905.1462193835"
                }
)
              
            except Exception,e:
                traceback.print_exc(file=open('tb.txt','w+'))


    def parse_article(self, response):
        url = response.url
        print response
        time_resp = "".join(response.xpath('//*[@id="Main"]/div[2]/div[1]/small/text()').extract())
        # now = time.strftime("%Y-%m-%d %X", time.localtime())
        try:
            time_day = time_resp.split(u' · ')[1].split(u'前')[0].strip().split(' ')
            if len(time_day) == 4:
                hour_bef = -int(time_day[0].strip())
                minute_bef = -int(time_day[2].strip())
                time_t = (datetime.now()+timedelta(hours=hour_bef,minutes=minute_bef)).strftime('%Y-%m-%d %X')
            elif len(time_day) == 2:
                # Some(or many) days before, maybe not so specific
                days_bef = -int(time_day[0].strip())
                time_t = (datetime.now()+timedelta(days=days_bef)).strftime('%Y-%m-%d %X')       
            else:
                time_t = ''
        except Exception, e:
            print time_resp
            time_t = ''
            traceback.print_exc(file=open('tb.txt','w+'))

   
        title = "".join(response.xpath('//*[@id="Main"]/div[2]/div[1]/h1/text()').extract())
      
        try:
            #It may has a div with the "outdated" class. (Low possibility~)
            if response.xpath('//div[@class="outdated"]'):
                contentwrapper = response.xpath('//*[@id="Main"]/div[2]/div[3]/div')
            else:
                contentwrapper = response.xpath('//*[@id="Main"]/div[2]/div[2]/div')
        except Exception,e:
            #Write the traceback info into a file.
            traceback.print_exc(file=open('tb.txt','w+'))

        content = "\n".join(contentwrapper.xpath('string(.)').extract())
        if (u'实习' in title) or (u'实习' in content):
            job_type = 'intern'
        else:
            job_type = 'job'
        
        mails = get_mail(content)
        email = mails[0] if mails else ''
        # TODO use machine learning to tag the info
        tags = 'a,b'

        item = JobItem()
        try:
            item['title'] = title
            item['url'] = url
            item['email'] = email
            item['content'] = content
            item['time'] = time_t
            item['tags'] = tags
            item['type'] = job_type
            yield item
        except Exception,e:
            traceback.print_exc()
  
