from sgmllib import SGMLParser
import urllib2


def get_news():
    news = []
    content = []
    images = []
    titlelist = SpiderTitleUrlTimes()
    titlelist.feed(get_html(
        'http://jwc.sdibt.edu.cn/SmallClass.asp?BigClassName=%D0%C5%CF%A2%B7%A2%B2%BC&SmallClassName=%D0%C2%CE%C5%B6%AF%CC%AC'))
    title = titlelist.get_title_list()
    time = titlelist.get_times()
    url = titlelist.get_url()
    for i in url:
        con = SpiderContent()
        con.feed(get_html(i))
        content.append(con.get_content())
        images.append('')
    for i in range(len(url)):
        news.append([title[i], content[i], 'jwc', url[i], time[i], images[i]])
    return news


def get_html(url):
    response = urllib2.urlopen(url)
    html = response.read()
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
            if k == 'class' and v == 'white_bg':
                h = [v for k, v in attrs if k == 'href']
                u = ''.join(h)
                self.url.append(u.decode('gbk').encode('utf-8'))
                self.flag = True

    def end_a(self):
        self.flag = False

    def start_font(self, attrs):
        for k, v in attrs:
            if k == 'color' and v == '#666666':
                self.timesFlag = True

    def end_font(self):
        self.timesFlag = False

    def handle_data(self, text):
        if self.flag:
            text = text.strip()
            self.titleList.append(text.decode('gbk').encode('utf-8'))
        if self.timesFlag:
            text = text.strip()
            self.t.append(text.decode('gbk').encode('utf-8'))

    def get_title_list(self):
        return self.titleList

    def get_times(self):
        for i in range(len(self.t)):
            if i % 2 == 0:
                self.times.append(self.t[i][1:-2])
        return self.times

    def get_url(self):
        for i in range(len(self.url)):
            self.url[i] = 'http://jwc.sdibt.edu.cn/' + self.url[i]
        return self.url


class SpiderContent(SGMLParser):
    def __init__(self):
        SGMLParser.reset(self)
        self.title = ''
        self.content = ''
        self.contentTd = ''
        self.titleFlag = False
        self.contentFlag = False
        self.contentTdFlag = False
        self.verbatim = 0

    def start_font(self, attrs):
        for k, v in attrs:
            if k == 'color' and v == '#000066':
                self.titleFlag = True

    def end_font(self):
        self.titleFlag = False

    def start_span(self, attrs):
        if self.contentFlag:
            self.verbatim += 1
            return
        self.contentFlag = True

    def end_span(self):
        if self.verbatim == 0:
            self.contentFlag = False
        if self.contentFlag:
            self.verbatim -= 1

    def start_td(self, attrs):
        for k, v in attrs:
            if k == 'style' and v == 'font-size:12px':
                self.contentTdFlag = True

    def end_td(self):
        self.contentTdFlag = False

    def handle_data(self, text):
        if self.titleFlag:
            text = text.strip()
            self.title = text.decode('gbk').encode('utf-8')
        if self.contentFlag:
            self.content += text.decode('gbk').encode('utf-8')
        if self.contentTdFlag:
            self.contentTd += text.decode('gbk').encode('utf-8')

    def get_title(self):
        return self.title

    def get_content(self):
        self.content = self.content.replace(' ', '')
        self.content = self.content.strip()
        if self.content == '':
            self.contentTd = self.contentTd.replace(' ', '')
            self.contentTd = self.contentTd.strip()
            return self.contentTd
        return self.content