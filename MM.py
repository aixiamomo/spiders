# coding=utf-8
import urllib2
import urllib
import requests
import re
from bs4 import BeautifulSoup
import os
import tool


class Spider(object):

	def __init__(self):
		self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'
		self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
		self.headers = {'User-Agent': 'self.user_agent'}
		self.tool = tool.Tool()

	def getPage(self, pageIndex):
		url = self.siteURL + '?page=' + str(pageIndex)
		print url
#		request = urllib2.Request(url)
#		response = urllib2.urlopen(request)
#		return response.read().decode('gbk')
		response = requests.get(url, headers=self.headers)
		return response.text

	def getContents(self, pageIndex):
		page = self.getPage(pageIndex)
		'''
		pattern = re.compile(
			'<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
		items = re.findall(pattern, page)
		for item in items:
			print item[0], item[1], item[2], item[3], item[4]
		'''
		soup = BeautifulSoup(page)
		item0 = []
		item1 = []
		item2 = []
		item3 = []
		item4 = []
		for i in soup.find_all(class_="lady-name"):
			href = 'http:' + i.get('href')
			item0.append(href)

		for i in soup.find_all(class_="lady-name"):
			name = i.string
			item1.append(name)

		for i in soup.find_all(height="60"):
			pic = 'http:' + i.get('src')
			item2.append(pic)

		for i in soup.find_all(class_="top"):
			age = i.strong.string
			item3.append(age)

		for i in soup.find_all(class_="top"):
			site = i.span.string
			item4.append(site)

		contents = zip(item0, item2, item1, item3, item4)
		return contents

	# 获取MM个人详情页面
	def getDetailPage(self, infoURL):
		response = urllib2.urlopen(infoURL)
		return response.read().decode('gbk')

	# 个人简介
	def getBrief(self, page):
		pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--', re.S)
		result = re.search(pattern, page)
		return self.tool.replace(result.group(1))

	def getAllImg(self, page):
		pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
		# 个人信息页面所有代码
		content = re.search(pattern,page)
		# 从代码中提取图片
		patternImg = re.compile('<img.*?src="(.*?)"',re.S)
		images = re.findall(patternImg,content.group(1))
		return images

	def saveImgs(self, images, name):
		number = 1
		print u'发现',name,u'共有', len(images), u'张照片'
		for imageURL in images:
			splitPath = imageURL.split('.')
			fTail = splitPath.pop()
			if len(fTail) > 3:
				fTail = "jpg"
			fileName = name + "/" + str(number) + "." + fTail
			self.saveImg(imageURL,fileName)
			number += 1

	def saveIcon(self, iconURL, name):
		splitPath = iconURL.split('.')
		fTail = splitPath.pop()
		fileName = name + "/icon." + fTail
		self.saveImg(iconURL,fileName)

	def saveImg(self, imageURL, fileName):
		u = urllib.urlopen(imageURL)
		data = u.read()
		f = open(fileName, 'wb')
		f.write(data)
		f.close()

	def saveBrief(self, content, name):
		fileName = name + '/' + name + '.txt'
		f = open(fileName, 'w+')
		print u'正在保存她的个人信息为', fileName
		f.write(content.encode('utf-8'))

	def mkdir(self, path):
		path = path.strip()
		isExists = os.path.exists(path)
		if not isExists:
			os.makedirs(path)
			return True
		else:
			return False

	def savePageInfo(self, pageIndex):
		# 获取第一页淘宝MM列表
		contents = self.getContents(pageIndex)
		for item in contents:
			# item[0]个人详情URL,item[1]头像URL,item[2]姓名,item[3]年龄,item[4]居住地
			print u"发现一位模特,名字叫",item[2],u"芳龄",item[3],u",她在",item[4]
			print u"正在偷偷地保存",item[2],"的信息"
			print u"又意外地发现她的个人地址是",item[0]
			# 个人详情页面的URL
			detailURL = item[0]
			# 得到个人详情页面代码
			detailPage = self.getDetailPage(detailURL)
			# 获取个人简介
			brief = self.getBrief(detailPage)
			# 获取所有图片列表
			images = self.getAllImg(detailPage)
			self.mkdir(item[2])
			# 保存个人简介
			self.saveBrief(brief,item[2])
			# 保存头像
			self.saveIcon(item[1],item[2])
			# 保存图片
			self.saveImgs(images,item[2])
 
	# 传入起止页码，获取MM图片
	def savePagesInfo(self,start,end):
		for i in range(start,end+1):
			print u"正在偷偷寻找第",i,u"个地方，看看MM们在不在"
			self.savePageInfo(i)



mm = Spider()
mm.savePagesInfo(2, 10)
