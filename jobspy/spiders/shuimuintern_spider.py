import scrapy
from jobspy.modules.mail import get_mail
from jobspy.modules.jobbean import *
from scrapy.http import Request
from jobspy.items import JobItem
from scrapy.utils.url import urljoin_rfc

class ShuimuInternSpider(scrapy.Spider):
    name = "shuimuintern"
    allowed_domains = ["m.newsmth.net"]
    start_urls = [
        "http://m.newsmth.net/board/ParttimeJobPost?p=1",
        "http://m.newsmth.net/board/ParttimeJobPost?p=2",
        "http://m.newsmth.net/board/ParttimeJobPost?p=3",
        "http://m.newsmth.net/board/ParttimeJobPost?p=4",
        "http://m.newsmth.net/board/ParttimeJobPost?p=5",
    ]

    def parse(self, response):
        articles = response.xpath('//ul[@class="list sec"]//li//div[1]//a')
        for article in articles:
            article_link = article.xpath('@href').extract()[0]
            article_url = urljoin_rfc('http://m.newsmth.net/', article_link)
            # manage duplicate url
            if [i for i in JobModel.where(url=article_url).select()]:
                return
            yield Request(url=article_url, callback=self.parse_article)

    def parse_article(self, response):
        url = response.url
        time = response.xpath('//div[@class="nav hl"][1]//a[@class="plant"][2]/text()')[0].extract()
        #time = time.strip()[:19]
        title = "".join(response.xpath('//ul[@class="list sec"]//li[1]/text()').extract())[3:]
        content = "\n".join(response.xpath('//ul[@class="list sec"]//div[@class="sp"][1]/text()')[:-2].extract())
        mails = get_mail(content)
        email = mails[0] if mails else ''
        # TODO use machine learning to tag the info
        tags = 'a,b'
        
        print url,time
        item = JobItem()
        item['title'] = title
        item['url'] = url
        item['email'] = email
        item['content'] = content
        item['time'] = time
        item['tags'] = tags
        item['type'] = 'intern'
        yield item 
        

