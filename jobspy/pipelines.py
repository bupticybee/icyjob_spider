# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
sys.path.append('/home/work/anaconda2/lib/python2.7/site-packages/')
import sklearn
from pypinyin import pinyin, lazy_pinyin
from jobspy.modules.jobbean import *
from jobspy.modules.simdup import *
from jobspy.modules.tagging import *
from hashes.simhash import simhash
from jobspy.modules.simdup import *

class JobspyPipeline(object):
    def process_item(self, item, spider):
        #,item['time']
	pinyin_content = ' '.join([i for i in lazy_pinyin(item['content'].strip()) if i.strip() ])
	pinyin_content = str(pinyin_content)
        #hashbits = simhash(item['content'], hashbits=32).hex()
        hashbits = simhash(pinyin_content, hashbits=64).hex()
        bitstr = str(bin(int(hashbits,16)))[3:]
        for i in range(64 - len(bitstr)):
            bitstr = '0' + bitstr
        
        print bitstr,len(bitstr)

        # manage duplicate url
        if [i for i in JobModel.where(url=item['url']).select()]:
            return item

        # manage duplicate content,using google simhash
        if has_dup(bitstr,item['time'],item['url']):
            return item
       
        insert_dup(bitstr,item['url'],item['time'])

        jobitem = JobModel()
        jobitem.title = item['title']
        jobitem.url = item['url']
        jobitem.email = item['email']
        jobitem.content = item['content']
        jobitem.time = item['time']
        jobitem.type = item['type']
        # jobitem.tags = item['tags']
        tagobj = Tag()
        itemtag = tagobj.gettag(item['content'],item['title'])

        jobtag = 'nontec'
        for tag in itemtag.split("\t"):
            if u'技术' in tag:
                jobtag = 'tec'
        jobitem.jobtag = jobtag
        jobitem.tags = str(itemtag)
        jobitem.save()

        # create tag if necessary
        tags = []
        for tag in itemtag.split("\t"):
            tagmodel = TagModel.where(tag=tag).select()
            if not [i for i in tagmodel]:
                tagmodel = TagModel()
                tagmodel.tag = tag
                tagmodel.save()

            tagmodel = TagModel.where(tag=tag).select()
            for i in tagmodel:
                tags.append(int(i.id))


        # save the tags
        for tag in tags:
            jobtagobj = JobCrossTagModel()
            jobtagobj.url = item['url']
            jobtagobj.tagid = tag
            jobtagobj.type = item['type']
            jobtagobj.time = item['time']
            jobtagobj.save()

        return item
