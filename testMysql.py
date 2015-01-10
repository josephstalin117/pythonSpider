import ssmysql
import spider

news = spider.get_news(
    'http://jwc.sdibt.edu.cn/SmallClass.asp?BigClassName=%D0%C5%CF%A2%B7%A2%B2%BC&SmallClassName=%D0%C2%CE%C5%B6%AF%CC%AC')
db = ssmysql.Db()
# db.insert_news('haha', 'nihao', 'jwc', 'baidu.com', '2015-2-16')

ssmysql.compare_news(news)
