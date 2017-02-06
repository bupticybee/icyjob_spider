 # -*- coding: utf-8 -*-
from jobbean import *
from tagging import *


#print [i for i in JobModel.where(time='2016-03-20 12:30:14').select()]

tagobj = Tag()
print tagobj.gettag(u'招聘python兼职实习',u'招聘兼职实习')
