import spider
from spider import get_html

titleList = spider.SpiderTitleUrlTimes()
html = get_html(
    'http://jwc.sdibt.edu.cn/SmallClass.asp?BigClassName=%D0%C5%CF%A2%B7%A2%B2%BC&SmallClassName=%D0%C2%CE%C5%B6%AF%CC%AC')
titleList.feed(html)
title = titleList.get_title_list()
time = titleList.get_times()
url = titleList.get_url()

for i in title:
    print i
for i in time:
    print i
for i in url:
    print i

title = spider.SpiderContent()
html2 = get_html(
    'http://jwc.sdibt.edu.cn/ReadNews.asp?NewsID=4271&BigClassName=%D0%C5%CF%A2%B7%A2%B2%BC&SmallClassName=%D0%C2%CE%C5%B6%AF%CC%AC&SpecialID=0')
title.feed(html2)
