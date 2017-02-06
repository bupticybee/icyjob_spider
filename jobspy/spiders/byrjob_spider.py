import scrapy
from jobspy.modules.mail import get_mail
from jobspy.modules.jobbean import *
from scrapy.http import Request
from jobspy.items import JobItem
from scrapy.utils.url import urljoin_rfc

class ByrJobSpider(scrapy.Spider):
    name = "byrjob"
    allowed_domains = ["m.byr.cn"]
    start_urls = [
        "http://m.byr.cn/board/JobInfo/6?p=1",
        "http://m.byr.cn/board/JobInfo/6?p=2",
        #"http://m.byr.cn/board/JobInfo/6?p=3",
        #"http://m.byr.cn/board/JobInfo/6?p=4",
        #"http://m.byr.cn/board/JobInfo/6?p=5",
    ]

    def start_requests(self):  
        for url in self.start_urls:          
            yield Request(url, cookies={
                    'nforum[PASSWORD]':'seheEHFPSZZhAF0%2B8cuRcg%3D%3D',
                    'nforum[UTMPKEY]':'28268958',
                    'nforum[UTMPNUM]':'2952',
                    'nforum[UTMPUSERID]':'icybee',
                })  

    def parse(self, response):
        articles = response.xpath('//ul[@class="list sec"]//li//div[1]//a')
        for article in articles:
            article_link = article.xpath('@href').extract()[0]
            article_url = urljoin_rfc('http://m.byr.cn/', article_link)
            # manage duplicate url
            if [i for i in JobModel.where(url=article_url).select()]:
                return
            yield Request(url=article_url, callback=self.parse_article, cookies={
                    'nforum[PASSWORD]':'seheEHFPSZZhAF0%2B8cuRcg%3D%3D',
                    'nforum[UTMPKEY]':'28268958',
                    'nforum[UTMPNUM]':'2952',
                    'nforum[UTMPUSERID]':'icybee',
                })

    def parse_article(self, response):
        url = response.url
        time = "".join(response.xpath('//a[@class="plant"]/text()').extract())
        title = "".join(response.xpath('//ul[@class="list sec"]//li[1]/text()').extract())[3:]
        content = "\n".join(response.xpath('//ul[@class="list sec"]//div[@class="sp"][1]/text()')[:-2].extract())
        mails = get_mail(content)
        email = mails[0] if mails else ''
        # TODO use machine learning to tag the info
        tags = 'a,b'
        
        item = JobItem()
        item['title'] = title
        item['url'] = url
        item['email'] = email
        item['content'] = content
        item['time'] = time
        item['tags'] = tags
        item['type'] = 'job'
        yield item 
        

