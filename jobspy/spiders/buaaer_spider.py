#-*-coding:utf8-*-
import scrapy 
from jobspy.modules.mail import get_mail
from jobspy.modules.jobbean import *
from scrapy.http import Request
from jobspy.items import JobItem
from scrapy.utils.url import urljoin_rfc

class BuaaerSpider(scrapy.Spider):
    name = 'buaaer'
    allowed_domains = ['www.buaaer.com']
    start_urls = [
	'http://www.buaaer.com/bbs/forumdisplay.php?fid=36&page=1',
	'http://www.buaaer.com/bbs/forumdisplay.php?fid=36&page=2'

	]

    def parse (self, response):
	start_num = 1
    	if response.url.split('page=')[1] == '1':
	    start_num = 3

    	for num in range(start_num,41):
    	    res_path = '/html/body/center/div[3]/table//center/form/div[1]/div[1]//table[%d]//td[@class="f_title"]//@href' %num
    	    item_link = response.xpath(res_path).extract()[0]
    	    item_url = urljoin_rfc('http://www.buaaer.com/bbs/',item_link)
	    if [i for i in JobModel.where(url=item_url).select()]:
		return
	    yield Request(url=item_url, callback=self.parse_article)
			
	

    def parse_article(self, response):
        url = response.url
	#print response.body	
	time = response.xpath('//form[@name="delpost"]/div[1]//table[@class="t_msg"]//tr[1]/td/div[1]/div[3]/text()').extract()[0].strip()[4:]+':00'
	title = ''.join(response.xpath('//tr[@class="header"]/td/text()').extract()).strip().split(u'标题:')[1].strip()
	contentwrapper = response.xpath('//form[@name="delpost"]/div[1]//table[@class="t_msg"]//div[@class="t_msgfont"]')
	content = '\n'.join(contentwrapper.xpath('string(.)').extract())
	mails = get_mail(content)
	email = mails[0] if mails else ''
	tags = 'a,b'
	if (u'实习' in content) or (u'兼职' in content):
	    types = 'intern'
	else:
	    types = 'job'

	item = JobItem()
	item['title'] = title
	item['url'] = url
	item['email'] = email
	item['content'] = content
	item['time'] = time
	item['tags'] = tags
	item['type'] = types
	yield item






