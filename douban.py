#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib,json
import urllib2
import cookielib
import gzip, StringIO

hostUrl = 'https://douban.fm'
loginUrl = 'https://accounts.douban.com/j/popup/login/basic'
getSongsInfoUrl = 'https://douban.fm/j/v2/redheart/basic'
getCookieUrl = 'https://douban.fm/j/check_loggedin?san=1'
getCookieUrl2 = 'https://www.douban.com/service/account/check_with_js?return_to=https%3A%2F%2Fdouban.fm%2Fj%2Fcheck_loggedin%3Fsan%3D1&sig=fef21efae8&r=0.2146490997849526&callback=_login_check_callback'
getSongsLinkUrl = 'https://douban.fm/j/v2/redheart/songs'

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

loginPostData = {
    'source': 'fm',
    'referer': 'https://douban.fm/',
    'ck': None,
    'name': 'funwewhere@foxmail.com',
    'password': '478505231dou',
    'captcha_solution': None,
    'captcha_id': None,
    'remember': 'on'
}

def sendRequest(request):
    response = urllib2.urlopen(request)
    responseInfo =  response.info()
    result = response.read()
    if 'Content-Encoding' in responseInfo and 'gzip' == responseInfo['Content-Encoding']:
        result = StringIO.StringIO(result)
        gz = gzip.GzipFile(fileobj=result)
        result = gz.read()
        gz.close()
    return result


if __name__ == '__main__':
    def domain_match(path, request):
        return True

    cookie = cookielib.CookieJar()
    cookie._policy.domain_return_ok = domain_match
    cookie._policy.return_ok_domain = domain_match

    cookieHandle = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(cookieHandle)
    urllib2.install_opener(opener)

    # try:
    sendRequest(urllib2.Request(hostUrl))
    sendRequest(urllib2.Request(loginUrl, urllib.urlencode(loginPostData), headers))
    sendRequest(urllib2.Request(getCookieUrl, headers=headers))
    sendRequest(urllib2.Request(getCookieUrl2, headers=headers))
    responseData = sendRequest(urllib2.Request(getSongsInfoUrl, headers=headers2))
    data = json.loads(responseData)

    songsInfos = [t['sid'] for t in data['songs']]
    postData = {
        'sids' : "|".join(songsInfos),
        'kbps': '320',
        'ck': [c.value for c in cookie if c.name == 'ck'][0]
    }
    responseData = sendRequest(urllib2.Request(getSongsLinkUrl, urllib.urlencode(postData), headers2))
    data = json.loads(responseData)

    for arr in data[0]:
        print arr,data[0][arr]

    for t in [{'title': t['title'], 'albumtitle':t['albumtitle'], 'album':t['album'], 'url': t['url']} for t in data]:
        print t
