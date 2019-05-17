# -*- coding: utf-8 -*-
import pymysql
# 用来操作数据库的类


class MySQLCommand(object):
    # 类的初始化
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306  # 端口号
        self.user = 'root'  # 用户名
        self.password = ""  # 密码
        self.db = "movie"  # 库
        self.table = "movie_list"  # 表

        # 链接数据库
    def connect_mysql(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, db=self.db, charset='utf8')
            self.cursor = self.conn.cursor()
        except Exception as e:
            print('connect mysql error.')

        # 插入数据，插入之前先查询是否存在，如果存在就不再插入
    def insert_data(self, my_dict):
        table = "movie_list"  # 要操作的表格
        # 注意，这里查询的sql语句href=' %s '中%s的前后要有空格
        sql_exit = "SELECT href FROM %s WHERE s_link = '%s'" % (table, my_dict['s_link'])
        res = self.cursor.execute(sql_exit)
        print(res)
        if res > 0:  # res为查询到的数据条数如果大于0就代表数据已经存在
            print("数据已存在，更新数据", my_dict['title'])
            sql = "UPDATE %s SET rate=%s WHERE s_link = '%s'" % (table, my_dict['rate'], my_dict['s_link'])
            self.cursor.execute(sql)
            self.conn.commit()
            return 0
        # 数据不存在才执行下面的插入操作
        try:
            cols = ', '.join(my_dict.keys())  # 用，分割
            # values = ', '.join(my_dict.values())
            values = '","'.join(str(v) for v in my_dict.values())
            sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, '"' + values + '"')
            # 拼装后的sql如下
            # INSERT INTO movie_list (img_path, url, id, title) VALUES ("https://img.huxiucdn.com.jpg"," https://www.huxiu.com90.html"," 12"," ")
            try:
                result = self.cursor.execute(sql)
                insert_id = self.conn.insert_id()  # 插入成功后返回的id
                self.conn.commit()
                # 判断是否执行成功
                if result:
                    print("插入成功", insert_id)
                    return insert_id + 1
            except pymysql.Error as e:
                # 发生错误时回滚
                self.conn.rollback()
                # 主键唯一，无法插入
                if "key 'PRIMARY'" in e.args[1]:
                    print("数据已存在，未插入数据")
                else:
                    print("插入数据失败，原因 %d: %s" % (e.args[0], e.args[1]))
        except pymysql.Error as e:
            print("数据库错误，原因%d: %s" % (e.args[0], e.args[1]))

    # 查询最后一条数据的id值
    def get_lastId(self):
        sql = "SELECT max(id) FROM " + self.table
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()  # 获取查询到的第一条数据
            if row[0]:
                return row[0]  # 返回最后一条数据的id
            else:
                return 0  # 如果表格为空就返回0
        except:
            print(sql + ' execute failed.')

    def close_mysql(self):
        self.cursor.close()
        self.conn.close()  # 创建数据库操作类的实例
