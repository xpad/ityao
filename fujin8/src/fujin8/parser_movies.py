#!/home/leo/Source/ldap_env/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import urllib2
import hashlib
import socket
import urlparse

sys.path.append('/home/leo/Source/ldap_env')
sys.path.append('/home/leo/Source/ityao/fujin8/src')
sys.path.append('/home/leo/Source/ityao/fujin8/src/fujin8')
os.environ['DJANGO_SETTINGS_MODULE'] = 'fujin8.settings'

from fujin8.btfactory.models import MonthlyLink, DailyLink, MovieLink
from django.db.utils import IntegrityError
from bt_parser import MonthlyCollectionParser, DailyCollectionParser


def getHTML(url=''):
    result = ''
    if url:
        # fake as normal web browser.
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0; GTB6.6; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; MASP)'}
        request = urllib2.Request(url, headers=headers)
        try:
            page = urllib2.urlopen(request)

            result = page.read().decode('gbk').encode('utf-8')
        except (urllib2.HTTPError, UnicodeDecodeError, socket.error), e:
            print '[exception]%s | [url]%s' % (str(e), url)
    return result


def parserMonthly():
    unparsed_monthly = MonthlyLink.objects.filter(enable=True)
    #unparsed_monthly = MonthlyLink.objects.all()
    for monthly in unparsed_monthly:
        r = urlparse.urlsplit(monthly.link)
        HTML = ''
        if monthly.raw_desc:
            HTML = monthly.raw_desc
        else:
            HTML = getHTML(monthly.link)
            monthly.raw_desc = HTML
            #monthly.save()

        if HTML:
            mcp = MonthlyCollectionParser()
            mcp.feed(HTML)

            for link in mcp.links:
                link_url, link_title = link
                link_url = urlparse.urlunsplit(('http', r.netloc, link_url, '', ''))
                daily = DailyLink(monthly_link=monthly, link=link_url, label=link_title)
                try:
                    daily.save()
                except IntegrityError:
                    # same move exists.
                    pass
        monthly.enable = False
        monthly.save()


def parserDaily():
    unparsed_dailys = DailyLink.objects.filter(parsed=False)
    #unparsed_dailys = DailyLink.objects.filter(id__gte=1, id__lt=10)
    #unparsed_dailys = DailyLink.objects.all()
    for daily in unparsed_dailys:
        HTML = ''
        if daily.raw_desc:
            HTML = daily.raw_desc
        else:
            HTML = getHTML(daily.link)
            daily.raw_desc = HTML

        if HTML:
            dcp = DailyCollectionParser()
            dcp.feed(HTML)
            for movie in dcp.all_movies:
                desc = ''
                digestkey = ''
                title = ''
                if movie.desc:
                    title = movie.desc[0]
                    desc = '\r\n'.join(movie.desc)
                    desc = desc.strip()
                    #import chardet
                    #print chardet.detect(desc)
                    #digestkey = hashlib.sha256(desc.decode('utf-8')).hexdigest()
                images = ';'.join(movie.imgs)
                downloadlink = ';'.join(movie.links)
                digestkey = hashlib.sha256(downloadlink).hexdigest()
                result = MovieLink.objects.filter(digestkey=digestkey)
                if not len(result):
                    # didn't exists same movie.
                    ml = MovieLink(title=title, raw_desc=desc, digestkey=digestkey, daily_link=daily, images=images, downloadlink=downloadlink)
                    ml.save()
                    '''
                    try:
                        ml = MovieLink(title=title, raw_desc=desc, digestkey=digestkey, daily_link=daily, images=images, downloadlink=downloadlink)
                        ml.save()
                    except Exception, e:
                        print '[%s]%s' % (title, str(e))
                        exit(1)
                    '''

        daily.parsed = True
        daily.save()
        # should not be banned by origin server.
        #import time
        #time.sleep(5)

def debugdaily():
    #unparsed_dailys = DailyLink.objects.filter(parsed=False)
    dl = DailyLink.objects.get(id=4)
    import chardet
    import re
    
    dcp = DailyCollectionParser()
    dcp.feed(dl.raw_desc)
    f = open('bt_parser.txt', 'w')
    for movie in dcp.all_movies:
        #f.write(' ^ '.join(movie.desc.encode('utf-8')))
        dd = []
        for d in movie.desc:
            dd.append(d.encode('utf-8'))
        f.write(' ^ '.join(dd))
        f.write('\r\n=======================\r\n')
        f.write(';'.join(movie.imgs))
        f.write('\r\n=======================\r\n')
        f.write(';'.join(movie.links))
        f.write("\r\n\r\n***********************\r\n\r\n")
    f.close()    


if __name__=='__main__':
    if sys.argv[1] == 'monthly':
        parserMonthly()
    elif sys.argv[1] == 'daily':
        parserDaily()
    elif sys.argv[1] == 'dbgdaily':
        debugdaily()
