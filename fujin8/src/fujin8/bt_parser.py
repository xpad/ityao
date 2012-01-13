#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sgmllib import SGMLParser
import re
import chardet

class MonthlyCollectionParser(SGMLParser):

    def __init__(self):
        SGMLParser.__init__(self)
        self.is_div = False
        self.is_a = False
        self.month_link = []
        self.links = []

    def start_div(self, attrs):
        id = [v for k, v in attrs if k == 'id']
        if id == ['content']:
            self.is_div = True

    def end_div(self):
        self.is_div = False

    def start_a(self, attrs):
        href = [v for k, v in attrs if k == 'href']

        if href[0].startswith('/p2p/'):
            self.month_link = href
            self.is_a = True

    def end_a(self):
        self.is_a = False

    def handle_data(self, data):
        if self.is_div and self.is_a:
            self.month_link.append(data.strip())
            self.links.append(self.month_link)


class Movie:

    def __init__(self):
        self.imgs = []
        self.links = []
        self.desc = []


class DailyCollectionParser(SGMLParser):

    def __init__(self):
        SGMLParser.__init__(self)
        self.is_div = False
        self.movie = Movie()
        self.all_movies = []
        self.is_movie_info_end = False
        #self.is_image_link = False
        #self.is_another_link = False
        self.download_link_pattern = re.compile(r'http://(?:\w+\.\w+?down\.info|filemarkets\.com|btroom1\.com)', re.I)
        self.another_link_pattern = re.compile(r'(?:\[)*(?:AVI|MP4|DVD|BD|WMV|HD|M2TS|MKV)', re.I)
        #self.image_link_pattern = re.compile(r'\.(jpg|jpeg|gif|png)$', re.I)
        #self.verify_code_parttern = re.compile(r'特徵代碼')

    # <div id="content">
    def start_div(self, attrs):
        id = [v for k, v in attrs if k=='id']
        if id == ['content']:
            self.is_div = True

    def end_div(self):
        self.is_div = False

    # <img src="...">
    def start_img(self, attrs):
        if self.is_div:
            src = [v for k, v in attrs if k=='src']
            self.movie.imgs.append(src[0])

    # <a href="...">
    def start_a(self, attrs):
        if self.is_div:
            href = [v for k, v in attrs if k == 'href']

            '''
            if href[0].startswith("http://item.slide.com/") or
                                re.search(self.image_link_pattern, href[0]):
                # a image link
                #self.is_image_link = True
                #self.movie.imgs.append(href[0])
                pass
            else:
                # a download link
                self.movie.links.append(href[0])
            '''
            if re.search(self.download_link_pattern, href[0]):
                self.movie.links.append(href[0])
                self.is_movie_info_end = True

    def end_a(self):
        if self.is_div:
            #self.is_image_link = False # reset
            if self.is_movie_info_end:
                # save info befor a new movie start.

                #if len(self.movie.desc) == 1 and len(self.movie.imgs) == 0 and re.match(self.another_link_pattern, self.movie.desc[0]):
                if len(self.movie.imgs) == 0:
                    # if the movie contains no images.

                    # if the movie only contains one-line description &
                    # only starts with 'HD', 'AVI', 'WMV' etc,
                    # the movie should be merged with last movie.
                    last_movie = self.all_movies[-1]
                    last_movie.desc.extend(self.movie.desc)
                    last_movie.links.extend(self.movie.links)
                    self.all_movies[-1] = last_movie
                else:
                    # a normal movie, put it into the pool.
                    self.all_movies.append(self.movie)
                # create new instance of Movie class.
                self.movie = Movie()
                # reset
                self.is_movie_info_end = False

    def handle_data(self, data):
        data = data.strip()
        if data and self.is_div:
            #if (u'點此下載' not in data.decode('utf-8')) and ('種子鏈接' not in data) and ('下載地址' not in data) and (not re.search('http:', data)):
            pattern_chinese = ur'點此下載|種子鏈接|下載地址|精彩回看|离线下载很给力'
            pattern_nochinese = r'^-*$|^\w+$|^$|http:|\[/url\]$'
            if not re.search(pattern_chinese, data) and not re.search(pattern_nochinese, data):
                self.movie.desc.append(data)
            '''
            if not self.is_image_link:
                if data.decode('utf-8') == u'*****點此下載*****' or \
                    re.match(self.download_link_pattern, data):
                    # download link. also means ends of a movie and
                    # should be start a new movie.
                    # known bugs: little movies has two or more dowload links,
                    # only first download link will be saved,
                    # other links after first download link will
                    # be recognized as a new movie
                    self.is_movie_info_end = True
                else:
                    self.movie.desc.append(data.decode('utf-8'))
                    '''

if __name__ == '__main__':
    import sys
    """
    import urllib2
    # fake as a normal web browser.
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    req = urllib2.Request('http://mi.10bt.info/00/01.html', headers=headers)
    page = urllib2.urlopen(req)
    """
    """
    parser = MonthlyCollectionParser()
    parser.feed(page.read())
    """
    """
    parser = MonthlyCollectionParser()
    parser.feed(MonthlyCollection)
    print parser.links
    """

    fh = open('test2.html', 'r')
    dc_content2 = fh.read()
    parser = DailyCollectionParser()
    parser.feed(dc_content2)
    movies = []
    if len(sys.argv) >=2:
        try:
            movie_idx = int(sys.argv[1])
            movie = parser.all_movies[movie_idx]
            movies.append(movie)
        except Exception:
            print 'The param must be a number.'
            exit(256)
    else:
        movies = parser.all_movies

    '''
    print(';'.join(movie.links))
    #print('\r\n')
    #print(';'.join(movie.imgs))

    for img in movie.imgs:
        try:
            req = urllib2.urlopen(img, timeout=5)
            img_size = int(req.info().getheader('Content-Length'))
            egrep_result = os.popen('egrep "\s%d$" media/images/images_list.txt' % img_size).readlines()

            if egrep_result:
                print img_size, egrep_result
        except urllib2.HTTPError, e:
            pass
    print('\r\n')
    #print('\r\n'.join(movie.desc))

    print('[hash title]:%s' % hashlib.sha1(movie.desc[0]).hexdigest())
    print('[hash desc]:%s' % hashlib.sha1(movie.links[0]).hexdigest())
    #print(hashlib.sha1('最新加勒比 083011-793 沒有比這更合適的了 前編 椎名ゆず').hexdigest())
    '''

    """
    movie = parser.all_movies[2]
    f = open('bt_parser.txt', 'w')
    f.writelines(movie.desc)
    f.write("\r\n***********************\r\n")
    f.write(';'.join(movie.links))
    f.write("\r\n***********************\r\n")
    f.write(';'.join(movie.imgs))
    f.close()
    """

    f = open('bt_parser.txt', 'w')
    for movie in movies:
        f.write(' ^ '.join(movie.desc))
        f.write('\r\n=======================\r\n')
        f.write(';'.join(movie.imgs))
        f.write('\r\n=======================\r\n')
        f.write(';'.join(movie.links))
        f.write("\r\n\r\n***********************\r\n\r\n")
    f.close()
    parser.close()
