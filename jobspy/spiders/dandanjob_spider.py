import scrapy
from jobspy.modules.mail import get_mail
from jobspy.modules.jobbean import *
from scrapy.http import Request
from jobspy.items import JobItem
from scrapy.utils.url import urljoin_rfc

# TODO a second database to cross the tag and the jobinfo

class DandanJobSpider(scrapy.Spider):
    name = "dandanjob"
    allowed_domains = ["www.oiegg.com"]
    start_urls = [
        "http://www.oiegg.com/forumdisplay.php?fid=101&page=1",
        "http://www.oiegg.com/forumdisplay.php?fid=101&page=2",
        #"http://www.oiegg.com/forumdisplay.php?fid=735&page=3",
        #"http://www.oiegg.com/forumdisplay.php?fid=735&page=4",
        #"http://www.oiegg.com/forumdisplay.php?fid=735&page=5",
    ]

    def parse(self, response):
        articles = response.xpath('//table[@id="forum_101"]//tbody/tr/th/span//a[2]')
        for article in articles:
            article_link = article.xpath('@href').extract()[0]
            article_url = urljoin_rfc('http://www.oiegg.com/', article_link)
            # manage duplicate url
            if [i for i in JobModel.where(url=article_url).select()]:
                return
            yield Request(url=article_url, callback=self.parse_article)

    def parse_article(self, response):
        url = response.url
        #time = "".join(response.xpath('//span[@class="post-list-info"][1]//a[1]/text()').extract()) + ":00"
        time = "".join(response.xpath('//div[@class="postinfo"][1]/text()').extract()).strip()[3:] + ":00"
        title = "".join(response.xpath('//h1/text()').extract())
        contentwrapper = response.xpath('//div[@class="t_msgfont"][1]')
        content = "\n".join(contentwrapper.xpath('string(.)').extract())
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
        

