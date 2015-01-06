from sgmllib import SGMLParser
import urllib2


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
        return self.url


class SpiderContent(SGMLParser):
    def __init__(self):
        SGMLParser.reset(self)
        self.title = ''
        self.con = []
        self.content = ''
        self.titleFlag = False
        self.contentFlag = False

    def start_font(self, attrs):
        for k, v in attrs:
            if k == 'color' and v == '#000066':
                self.titleFlag = True

    def end_font(self):
        self.titleFlag = False

    def start_span(self, attrs):
        self.contentFlag = True

    def end_span(self):
        self.contentFlag = False

    def handle_data(self, text):
        if self.titleFlag:
            text = text.strip()
            self.title = text.decode('gbk').encode('utf-8')
        if self.contentFlag:
            self.con.append(text.decode('gbk').encode('utf-8'))

        self.content = ''.join(self.con)

    def get_title(self):
        return self.title

    def get_content(self):
        return self.con