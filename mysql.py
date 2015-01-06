import MySQLdb


try:
    conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='test', port=3306)
    cur = conn.cursor()
    cur.execute('select * from test')
    results = cur.fetchall()
    for r in results:
        print r
    cur.close()
    conn.close()
except MySQLdb.Error, e:
    print "Mysql Error %d: %s" % (e.args[0], e.args[1])