#!-*-coding: UTF-8 -*-
from sgmllib import SGMLParser
import urllib2
import re


def get_news():
    news = []
    content = []
    image = []
    titlelist = SpiderTitleUrlTimes()
    titlelist.feed(get_html('http://ccec.edu.cn/list.php?fid=7'))
    title = titlelist.get_title_list()
    time = titlelist.get_times()
    url = titlelist.get_url()

    for i in url:
        con = SpiderContent()
        con.feed(get_html(i))
        content.append(con.get_content())
        image.append(con.get_image())
    for i in range(len(url)):
        news.append([title[i], content[i], 'ccec', url[i], time[i], image[i]])
    return news


def get_html(url):
    response = urllib2.urlopen(url)
    html = re.sub('onload=\'\s*[^\"]*\'', '', response.read())
    return html


class SpiderTitleUrlTimes(SGMLParser):
    def __init__(self):
        SGMLParser.reset(self)
        self.titleList = []
        self.url = []
        self.t = []
        self.times = []
        self.flag = False
        self.timesFlag = False

    def start_a(self, attrs):
        for k, v in attrs:
            if k == 'target' and v == '_self':
                h = [v for k, v in attrs if k == 'href']
                u = ''.join(h)
                self.url.append(u.decode('gbk').encode('utf-8'))
                self.flag = True

    def end_a(self):
        self.flag = False

    def start_span(self, attrs):
        for k, v in attrs:
            if k == 'class' and v == 'time':
                self.timesFlag = True

    def end_span(self):
        self.timesFlag = False

    def handle_data(self, text):
        if self.flag:
            text = text.strip()
            self.titleList.append(text.decode('gbk').encode('utf-8'))
        if self.timesFlag:
            text = text.strip()
            self.t.append(text.decode('gbk').encode('utf-8'))

    def get_title_list(self):
        return self.titleList[6:]

    def get_times(self):
        for i in range(len(self.t)):
            self.times.append(self.t[i][1:-1])
        return self.times

    def get_url(self):
        for i in range(len(self.url)):
            self.url[i] = 'http://ccec.edu.cn/' + self.url[i]
        return self.url[7:]


class SpiderContent(SGMLParser):
    def __init__(self):
        SGMLParser.reset(self)
        self.content = ''
        self.contentTd = ''
        self.image = ''
        self.imageFlag = False
        self.contentFlag = False
        self.contentTdFlag = False
        self.verbatim = 0

    def start_td(self, attrs):
        for k, v in attrs:
            if k == 'style' and v == 'line-height:25px; color:#333333; font-size:12px; text-align:left;':
                self.contentTdFlag = True

    def end_td(self):
        self.contentTdFlag = False

    def start_span(self, attrs):
        if self.contentTdFlag:
            if self.contentFlag:
                self.verbatim += 1
                return
            self.contentFlag = True

    def end_span(self):
        if self.contentTdFlag:
            if self.verbatim == 0:
                self.contentFlag = False
            if self.contentFlag:
                self.verbatim -= 1

    def start_img(self, attrs):
        if self.contentTdFlag:
            for k, v in attrs:
                if k == 'src':
                    self.image = v

    def end_img(self):
        if self.contentTdFlag:
            self.imageFlag = False

    def handle_data(self, text):
        if self.contentFlag:
            self.content += text.decode('gbk').encode('utf-8')

    def get_image(self):
        return self.image

    def get_content(self):
        self.content = self.content.strip()
        return self.content