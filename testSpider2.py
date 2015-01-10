import spider
from spider import get_html, get_news

news = spider.get_news(
    'http://jwc.sdibt.edu.cn/SmallClass.asp?BigClassName=%D0%C5%CF%A2%B7%A2%B2%BC&SmallClassName=%D0%C2%CE%C5%B6%AF%CC%AC')

print len(news)

for i in news:
    print i[4]