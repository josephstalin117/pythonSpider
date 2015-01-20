#!/usr/bin/python
import ssmysql
import spiderJwc
import spiderCcec

news = spiderJwc.get_news()
news = ssmysql.compare_news(news, 'jwc')
ssmysql.insert_news(news)

news = spiderCcec.get_news()
news = ssmysql.compare_news(news, 'ccec')
ssmysql.insert_news(news)