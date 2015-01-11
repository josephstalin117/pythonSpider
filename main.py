import ssmysql
import spider

news = spider.get_news(
    'http://jwc.sdibt.edu.cn/SmallClass.asp?BigClassName=%D0%C5%CF%A2%B7%A2%B2%BC&SmallClassName=%D0%C2%CE%C5%B6%AF%CC%AC')
news = ssmysql.compare_news(news)
ssmysql.insert_news(news)
