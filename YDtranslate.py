#coding=utf-8
import urllib2
import urllib
import json
import time

while True:
    content = raw_input('请输出需要翻译的内容：(输入"q!"退出程序)')
    if content == 'q!':
        break
    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=https://www.google.co.jp/"
    data = {}

    data['type']= 'AUTO'
    data['i']= content

    data['doctype']='json'
    data['xmlVersion']='1.8'
    data['keyfrom']='fanyi.web'
    data['ue']='UTF-8'
    data['action']='FY_BY_CLICKBUTTON'
    data['typoResult']='true'

    data = urllib.urlencode(data).encode('utf-8')

    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4"


    request = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(request)

    fanyi = response.read().decode('utf-8')

    target = json.loads(fanyi)

    a = target['translateResult'][0][0]['tgt']
    print u"翻译结果：%s" % a

    time.sleep(2)
    # with open('web.html', 'w') as f:
    #    f.write(response.read().decode('utf-8'))


