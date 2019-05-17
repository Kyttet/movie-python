from bs4 import BeautifulSoup
from urllib import request
from urllib.parse import quote
import string
from db.MySQLCommand import MySQLCommand



def get_list(page):
	url = "http://www.wuhaozhan.net/movie/list/?p=%d" % page
	response = request.urlopen(url)
	html = response.read()

	# 使用剖析器为html.parser
	soup = BeautifulSoup(html, 'html.parser')
	# 获取列表容器节点
	all_list = soup.select('.l-box')
	# 遍历列表，获取有效信息
	for news in all_list:
		aaa = news.select('.l-a')
		# item_dict = {}
		# 只选择长度大于0的结果
		if len(aaa) > 0:
			# 文章链接
			try:  # 如果抛出异常就代表为空
				href = aaa[0]['href']
			except Exception as e:
				print('文章链接为空', e)
				href = ''
			# 文章图片url
			try:
				img_url = news.select('img')[0]['data-original']
			except Exception as e:
				print('图片URL为空', e)
				img_url = ""
			# 新闻标题
			try:
				title = aaa[0].string
			except Exception as e:
				print('标题为空', e)
				title = "标题为空"
			# 豆瓣评分
			try:
				rate = news.select('.l-average')[0].string
			except Exception as e:
				print('暂无评分', e)
				rate = -1

			item_dict = {
				'title': title,
				'href': href,
				'img_url': img_url,
				'rate': rate
			}
			get_detail(href, item_dict)




def get_detail(url,dict):
	# https://blog.csdn.net/sijiaqi11/article/details/78449770
	# https://docs.python.org/zh-cn/3/library/urllib.parse.html#urllib.parse.urlparse
	# urllib.request.urlopen不支持中英文混合的字符串
	# 使用urllib.parse.quote进行转换
	s = quote(url, safe=string.printable)
	response = request.urlopen(s)
	html = response.read()
	soup = BeautifulSoup(html, 'html.parser')
	resource_link = soup.select('.more-search')
	if len(resource_link):
		resource_link = soup.select('.more-search')[0].a['href']
		# print(resource_link)
		get_detail(resource_link,dict)
	else:
		try:
			resource_title = soup.select('.s-box')[0].find_all("div", string='迅雷下载')
			resource_list = resource_title[0].find_next_siblings('ul')
			resource_list = resource_list[0].select('.m_list')
		except Exception as e:
			resource_list = []
		global dataCount
		for link in resource_list:
			dict['s_link'] = link.a['href']
			dict['s_title'] = link.a.string
			dataCount = int(mysqlCommand.get_lastId()) + 1
			dict['id'] = str(dataCount)

			try:
				# 插入数据，如果已经存在就不在重复插入
				res = mysqlCommand.insert_data(dict)
				if res:
					dataCount = res
			except Exception as e:
				print("插入数据失败", str(e))  # 输出插入失败的报错语句

# 连接数据库
mysqlCommand = MySQLCommand()
mysqlCommand.connect_mysql()

# 这里每次查询数据库中最后一条数据的id，新加的数据每成功插入一条id+1
# movie_list = []
for page in range(20):
	get_list(page + 1)

mysqlCommand.close_mysql()  # 最后一定要要把数据关闭
dataCount = 0
