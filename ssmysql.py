import MySQLdb
import spider
from datetime import *
import time


def compare_news(news):
    # @todo
    db = Db()
    # the index list of expired news
    popList = []
    # for i in news:
    # print i[4]
    print db.lastTime
    print '#####################################################'
    for i in range(len(news)):
        # @todo
        if time.mktime(time.strptime(str(news[i][4]), '%Y-%m-%d')) < db.lastTime:
            popList.append(i)
    print popList
    return news


class Db:
    def __init__(self):
        self.title = []
        self.times = []
        self.lastTime = ''
        self.lastTimeIndex = ''
        self.result = []
        try:
            self.conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='ssnews', port=3306)
            self.cur = self.conn.cursor()
            self.search_latest_time()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def search_latest_time(self):
        self.cur.execute("select title,time from news")
        self.result = self.cur.fetchall()
        for row in self.result:
            self.title.append(row[0])
            self.times.append(time.mktime(time.strptime(str(row[1]), '%Y-%m-%d %H:%M:%S')))
        self.lastTime = max(self.times)
        self.lastTimeIndex = self.times.index(max(self.times))

    # @todo
    def compare_title(self):
        return

    def insert_news(self, title, content, tag, url, time):
        sql = "INSERT INTO news(title,content,tag,url,time) values(%s,%s,%s,%s,%s)"
        n = self.cur.execute(sql, (title, content, tag, url, time))
        print n
        id = self.cur.lastrowid
        self.conn.commit()
        return id

    def __del__(self):
        self.cur.close()
        self.conn.close()