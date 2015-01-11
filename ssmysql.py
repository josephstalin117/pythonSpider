import MySQLdb
import time


def compare_news(news):
    db = Db()
    # the index list of expired news
    expired = 0
    for i in range(len(news)):
        if time.mktime(time.strptime(str(news[i][4]), '%Y-%m-%d')) <= db.lastTime:
            expired = i
            break
    del news[expired:]
    return news


def insert_news(news):
    db = Db()
    return db.insert_news(news)


class Db:
    def __init__(self):
        self.title = []
        self.lastTime = ''
        self.lastTimeIndex = ''
        self.lastTitle = []
        self.result = []
        try:
            self.conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='ssnews', port=3306,
                                        charset="utf8")
            self.cur = self.conn.cursor()
            self.search_latest_time()
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def search_latest_time(self):
        self.cur.execute("SELECT time FROM news WHERE time IN (SELECT MAX(time) FROM news)")
        self.result = self.cur.fetchall()
        for row in self.result:
            self.lastTime = time.mktime(time.strptime(str(row[0]), '%Y-%m-%d %H:%M:%S'))

    def insert_news(self, news):
        if news:
            sql = "INSERT INTO news(title,content,tag,url,time) values(%s,%s,%s,%s,%s)"
            for i in news:
                self.cur.execute(sql, (i[0], i[1], i[2], i[3], i[4]))
            self.conn.commit()
            return self.cur.lastrowid
        return

    def __del__(self):
        self.cur.close()
        self.conn.close()