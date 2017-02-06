import jieba
import sys,os
reload(sys)
sys.setdefaultencoding("utf-8")

class Tag:
    def cur_file_dir(self):
        return os.path.split(os.path.realpath(__file__))[0]

    def __init__(self):
        currentdir = self.cur_file_dir() 
        conffile = os.path.join(currentdir,'../conf/tags')

        self.tagdic = {}
        with open(conffile) as fhdl:
            for line in fhdl:
                linesp = line.split("\t")
                tag = linesp[0] + '_' + linesp[1]
                words = linesp[1:]
                words = [i.split(' ') for i in words]
                self.tagdic[tag] = words

    def gettag(self,query,title):
        rettags = []
        words = jieba.cut(title + " " + query)
        worddic = {}
        for word in words:
            word = word.encode("utf-8")  
            worddic[word] = 1
        for tag in self.tagdic:
            if tag in rettags:
                continue
            wordlists = self.tagdic[tag]
            for wordlist in wordlists:
                for word in wordlist:
                    missFlag = False
                    if word not in worddic:
                        missFlag = True
                if missFlag == False:
                    rettags.append(tag)
        return "\t".join(list(set(rettags)))
             

