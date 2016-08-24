#coding=utf-8
import os
import re
import urllib
import urllib2
from bs4 import BeautifulSoup
import requests
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

class Hospital(object):
	def __init__(self):
		self.url = 'http://www.guahao.com/hospital/ef30a81d-f12a-43de-8876-48e9292474f5000'
		self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'
		self.headers = {'User-Agent': 'self.user_agent'}

	# 获取页面代码
	def getPage(self, url):
		response = requests.get(url, headers=self.headers)
		return response.text

	# 获取大科室
#	def first_keshi(self):
#		page = self.getPage()
#		soup = BeautifulSoup(page)
#		hospital_Name = soup.find('li', class_="g-clear")
#		keshi_name = hospital_Name.label.string.strip()

	# 获取{'一级科室':[url1,url2...],...}
	def getContents(self):
		page = self.getPage(self.url)
		soup = BeautifulSoup(page, 'html.parser')
		result = {}
		li_html = soup.find_all('li', class_="g-clear")
		# 获取一级科室内的所有HTML代码
		for li in li_html:
			# 获取一级科室名
			key = li.label.string.strip()
			print key
			result[key] = []
			# 获取url列表
			for href in set(li.find_all(attrs={"data-nor":"1"})) | set(li.find_all(attrs={"data-exp":"1"})):
				result[key].append(href.a.get('href'))  # 获取细分科室的url
		return result


#	def getContents(self):
#		page = self.getPage(self.url)
#		soup = BeautifulSoup(page)
#		keshi_url = []
#		for a in soup.find_all('a', class_="ishao"):
#			keshi_url.append(a.get('href'))
#		return keshi_url
#			 科室名
#			print a.string.strip()

	def get_keshi_name(self, url_keshi):
		page = self.getPage(url_keshi)
		pattern = re.compile('<h1>(.*?)<label>', re.S)
		keshi_name = re.search(pattern, page).group(1)
		return keshi_name


	def get_Doctors(self, url_keshi):
		page = self.getPage(url_keshi)
		soup = BeautifulSoup(page)
		contents = []
		for a in soup.find_all(class_="g-clear g-doc-info", limit=3):
			name = a.a.img.get('alt')
			pic = 'http:' + a.a.img.get('src')
			try:
				zhiwei = a.dt.span.string
			except AttributeError:
				zhiwei = ' '
			jieshao = a.dd.p.get('title')
			contents.append([name, pic, zhiwei, jieshao])
		return contents

	def saveImg(self, imageURL, filename):
		u = urllib.urlopen(imageURL)
		data = u.read()
		f = open(filename + '.jpg', 'wb')
		f.write(data)
		f.close()

	def saveInfo(self, name, zhiwei, jieshao):
		content = zhiwei + '\n' + jieshao
		fileName = name + '.txt'
		f = open(fileName, 'w+')
		print u'正在保存个人信息为', fileName
		f.write(content.encode('utf-8'))		


	def second_keshi(self):
		soup = BeautifulSoup(self.getPageCode())
		print soup.find('c')

	def mkdir(self):
		filename = self.First_keshi()
		os.mkdir(filename)

	# 获取医院名
	def getHospital(self):
		page = self.getPage(self.url)
		soup = BeautifulSoup(page)
		a = soup.find(class_="detail word-break")
		return a.h1.strong.string

	def start(self):
		#self.mkdir()
		keshi_dict = self.getContents()
		# 创建医院目录
		hospital = self.getHospital()
		os.mkdir(hospital)
		os.chdir(hospital)
		for department in keshi_dict:
			os.mkdir(department)
			os.chdir(department)
			for url in keshi_dict[department]:
				print url
				items = self.get_Doctors(url)
				keshi_name = self.get_keshi_name(url)
				os.mkdir(keshi_name)
				os.chdir(keshi_name)
				for item in items:
					self.saveImg(item[1], item[0])
					self.saveInfo(item[0], item[2], item[3])
				os.chdir('..')
			os.chdir('..')




#		for i in keshi_url:
#			打开链接, 获得医生信息
#			items = self.get_Doctors(i)
#			keshi_name = self.get_keshi_name(i)
#			path = 'C:\\Users\\vip\\Desktop\\momo\\web_spider\\test\\' + keshi_name
#			os.chdir('C:\\Users\\vip\\Desktop\\momo\\web_spider\\test\\')
#			os.mkdir(keshi_name)
#			os.chdir(keshi_name)
#			for item in items:
#				self.saveImg(item[1], item[0])
#				self.saveInfo(item[0], item[2], item[3])
#			os.chdir('..')

'''
			获取代码信息

			创建科室目录
			进入科室目录
			保存图片
			保存信息
'''

			

if __name__ == '__main__':
	a = Hospital()
	a.start()
		
