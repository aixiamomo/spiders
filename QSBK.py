# coding=utf-8

import re
import urllib
import urllib2


class QSBK(object):

    """docstring for QSBK"""
    # 初始化方法，定义变量

    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'
        self.headers = {'User-Agent': 'self.user_agent'}
        # 存放段子的全局变量
        self.duanzi = []
        self.enable = False

    # 传入某一页的索引获得页面代码
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            # 将页面转化成utf-8编码，此时pageCode只是函数内的局部变量，值是getPage函数的返回值
            content = response.read().decode('utf-8')
            return content
        except urllib.URLError, e:
            if hasattr(e, 'reason'):
                print u'连接糗事百科失败，错误原因：', e.reason
                return None

    # 传入页面代码，返回本页不带图片的段子列表
    def getPageItems(self, pageIndex):
        # getpage函数的返回值被赋值给pageCode
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print u'页面加载失败...(つω｀)～'
            return None
        """
		.*?匹配任意无限多个字符，加上?表示非贪婪
		(.*?)表示分组，这个正则分了三组：作者，内容，有无图片，被赞的次数
		re.S 将. 变成任意匹配模式，也可以匹配换行
		"""
        pattern = re.compile('<h2>(.*?)</h2>.*?<div.*?"content">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</.*?>', re.S)
        items = re.findall(pattern, pageCode)
        # 存储每页的段子
        pageDuanzi = []
        # 剔除图片段子
        for item in items:
            haveImg = re.search('img', item[2])
            if not haveImg:
                # 替换段子内的换行符
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR, "\n", item[1])
                # item[0]作者，item[1]内容, item[2]有无图片, item[3]赞
                # strip()没参数，删除字符串中的开头、结尾的删除空白符（包括'\n', '\r',  '\t',  ' ')
                pageDuanzi.append(
                    [item[0].strip(), text.strip(), item[3].strip()])
        return pageDuanzi

    # 加载并提取页面内容，加入到列表中
    def loadPage(self):
        # 如果当前未看页数少于两页，加载新一页
        if self.enable == True:
            if len(self.duanzi) < 2:
                # 获取新一页
                pageStroies = self.getPageItems(self.pageIndex)
                # 将该页的段子存放到全局list中
                if pageStroies:
                    self.duanzi.append(pageStroies)
                    # 获取完成后页码+1，表示下次读取下一页
                    self.pageIndex += 1

    # 回车输出一个段子
    def getOneDuanzi(self, pageDuanzi, page):
        for story in pageDuanzi:
            # 等待用户输入
            input = raw_input()
            # 每当输入回车一次，判断是否要加载新页面
            self.loadPage()
            # Q退出程序
            if input == 'Q':
                self.enable = False
                return
            print u'第%d页\t发布人:%s\t赞:%s\n%s' % (page, story[0], story[2], story[1])

    # 开始方法
    def start(self):
        print u"- ( ゜- ゜)つロ 正在读取糗事百科，按回车查看新段子，输入'Q'退出"
        # 使变量为True, 程序可以运行
        self.enable = True
        # 加载一页内容
        self.loadPage()
        # 局部变量，控制当前读取到了第几页
        nowPage = 0
        while self.enable:
            if len(self.duanzi) > 0:
                # 从全局list中获取一页的段子
                pageDuanzi = self.duanzi[0]
                # 当前读到的页数+1
                nowPage += 1
                # 将全局list中的第一个元素删除，因为已经取出
                del self.duanzi[0]
                # 输出该页的段子
                self.getOneDuanzi(pageDuanzi, nowPage)

if __name__ == '__main__':
    spider = QSBK()
    spider.start()
