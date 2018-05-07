#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib,ssl
import urllib2
import cookielib
import gzip, StringIO

def req(r, opener):
    url = r.get_full_url()
    print '\n'+url
    response = opener.open(r)
    responseInfo =  response.info()
    data = response.read()
    print responseInfo
    if 'Content-Encoding' in responseInfo and 'gzip' == responseInfo['Content-Encoding']:
        data = StringIO.StringIO(data)
        gz = gzip.GzipFile(fileobj=data)
        data = gz.read()
        gz.close()

    print '\n'
    for ck in cj:
        print ck.name + ':' + ck.value
    print '\n'

    print data
    print url+'\n'

# 登录的主页面
hosturl = 'https://douban.fm'
loginurl = 'https://accounts.douban.com/j/popup/login/basic'
songsUrl = 'https://douban.fm/j/v2/redheart/basic'
cookieUrl = 'https://douban.fm/j/check_loggedin?san=1'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Referer': 'https://accounts.douban.com/popup/login?source=fm&use_post_message'
}

headers2 = {
    'Host': 'douban.fm',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

postData = {
    'source': 'fm',
    'referer': 'https://douban.fm/',
    'ck': None,
    'name': 'username',
    'password': 'pwd',
    'captcha_solution': None,
    'captcha_id': None,
    'remember': 'on'
}
postData = urllib.urlencode(postData)

cj = cookielib.CookieJar()
# cj.set_policy(policy)
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support)
urllib2.install_opener(opener)

req1 = urllib2.Request(hosturl)
req2 = urllib2.Request(loginurl, postData, headers)
req3 = urllib2.Request(cookieUrl, headers=headers)
req4 = urllib2.Request('https://www.douban.com/service/account/check_with_js?return_to=https%3A%2F%2Fdouban.fm%2Fj%2Fcheck_loggedin%3Fsan%3D1&sig=fef21efae8&r=0.2146490997849526&callback=_login_check_callback', headers=headers)
req5 = urllib2.Request(cookieUrl, headers=headers)
req6 = urllib2.Request(songsUrl, headers=headers2)

try:
    req(req1, opener)
    req(req2, opener)
    req(req3, opener)
    req(req4, opener)
    req(req5, opener)
    req(req6, opener)
except Exception,e:
    print Exception,":",e