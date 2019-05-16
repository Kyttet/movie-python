from bs4 import BeautifulSoup
from urllib import request
# import time
from db.MySQLCommand import MySQLCommand


def get_list(page):
	url = "http://www.wuhaozhan.net/movie/list/?p=%d" % page
	# print(url)
	response = request.urlopen(url)
	# time.sleep(3)
	html = response.read()
	# charset = chardet.detect(html)
	# html = html.decode(str(charset["encoding"]))  # 设置抓取到的html的编码方式

	# 使用剖析器为html.parser
	soup = BeautifulSoup(html, 'html.parser')
	# 获取到每一个class=hot-article-img的a节点
	all_list = soup.select('.l-box')
	global dataCount
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
				href=''
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
				rate = "暂无评分"
			dataCount = int(mysqlCommand.getLastId()) + 1
			item_dict = {
				'title': title,
				'href': href,
				'img_url': img_url,
				'id': str(dataCount),
				'rate': rate
			}
			try:
				# 插入数据，如果已经存在就不在重复插入
				res = mysqlCommand.insertData(item_dict)
				if res:
					dataCount = res
			except Exception as e:
				print("插入数据失败", str(e))  # 输出插入失败的报错语句
			# movie_list.append(item_dict)
			# print("标题",title,"\nurl：",href,"\n图片地址：",img_url)

# 连接数据库


mysqlCommand = MySQLCommand()
mysqlCommand.connectMysql()

# 这里每次查询数据库中最后一条数据的id，新加的数据每成功插入一条id+1
# movie_list = []
for page in range(1):
	get_list(page + 1)

mysqlCommand.closeMysql()  # 最后一定要要把数据关闭
dataCount = 0
