#!/usr/bin/python  
#coding=utf-8  

import urllib
import urllib2
import cookielib

def post(url, data):
    filename = 'nahcookie.txt'
    #cookie = cookielib.CookieJar()
    cookie = cookielib.MozillaCookieJar(filename)

    #enable cookie  
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    postdata = urllib.urlencode(data)
    response = opener.open(url, postdata)
    cookie.save(ignore_discard=True, ignore_expires=True)
    for item in cookie:
        print 'Name = '+item.name
        print 'Value = '+item.value
    return response.read()

def main():
    posturl = "http://bbs.byr.cn/user/ajax_login.json"
    data = {'id':'notahacker','passwd':'notahacker'}
    print post(posturl, data)

if __name__ == '__main__':
    main()
