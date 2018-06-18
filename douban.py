#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib,json,os,sys
import urllib2,re
import cookielib,threading
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
    'name': None,
    'password': None,
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


def Schedule(a,b,c):
    rate = 1.0 * a * b / c
    rate_num = int(rate * 100)
    number = int(50 * rate)
    r = '\r[%s%s]%d%%' % ("=" * number, " " * (50 - number), rate_num)
    print "\r {}".format(r),
    
def initCookieHandle():
    def domain_match(path, request):
        return True
    cookie = cookielib.CookieJar()
    cookie._policy.domain_return_ok = domain_match
    cookie._policy.return_ok_domain = domain_match
    cookieHandle = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(cookieHandle)
    urllib2.install_opener(opener)
    return cookie

def main():
    cookie = initCookieHandle();

    print 'please input douban account info'
    loginPostData['name'] = raw_input("username: ")
    loginPostData['password'] = raw_input("password: ")

    sendRequest(urllib2.Request(hostUrl))
    sendRequest(urllib2.Request(loginUrl, urllib.urlencode(loginPostData), headers))
    sendRequest(urllib2.Request(getCookieUrl, headers=headers))
    sendRequest(urllib2.Request(getCookieUrl2, headers=headers))

    responseData = sendRequest(urllib2.Request(getSongsInfoUrl, headers=headers2))
    data = json.loads(responseData)
    songsInfos = [t['sid'] for t in data['songs']]

    if not 'Y' == raw_input('you have ' + str(len(songsInfos)) + ' songs, Do you want to download? Y/N:'):
        print('exit!')
        sys.exit(0)

    savePath = raw_input("please input the path you want to save music file(like D:/Downloads or /usr/local):")
    if (len(savePath)>0 and not (savePath.endswith("/") or savePath.endswith("\\"))):
        savePath = savePath +'/'

    postData = {
        'sids': "|".join(songsInfos),
        'kbps': '320',
        'ck': [c.value for c in cookie if c.name == 'ck'][0]
    }
    responseData = sendRequest(urllib2.Request(getSongsLinkUrl, urllib.urlencode(postData), headers2))
    data = json.loads(unicode(responseData, "utf-8"))

    failDownloadSongs = [];

    for item in data:
        i = 1
        fileSaveName = item['artist'] + ' - ' + item['title'] + item['url'][item['url'].rfind('.'):len(item['url'])]
        while os.path.exists(savePath + fileSaveName):
            fileSaveName = fileSaveName = item['artist'] + ' - ' + item['title'] + ' - ' + str(i) + item['url'][item['url'].rfind('.'):len(item['url'])]
            i += 1
        item['fileSaveName'] = re.sub('[\\\\\/:*?"<>|]', '-', fileSaveName)
        print 'start download [%s][%s]' % (item['fileSaveName'], item['url'])
        try:
            urllib.urlretrieve(item['url'], savePath + item['fileSaveName'], Schedule)
            print ''
        except:
            failDownloadSongs.append(item)
            print 'fail to download [' + item['fileSaveName'] + '] url [' + item['url'] + ']'

    print 'done!'
    
    if (len(failDownloadSongs)>0):
        for item in failDownloadSongs:
            print item['fileSaveName'] + ', ' + item['url']

if __name__ == '__main__':
    main()