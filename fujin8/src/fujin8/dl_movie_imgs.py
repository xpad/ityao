#!/home/leo/Source/ldap_env/bin/python
import os
import os.path
import re
import sys
import socket
import urllib

sys.path.append('/home/leo/Source/ldap_env')
sys.path.append('/home/leo/Source/ityao/fujin8/src')
sys.path.append('/home/leo/Source/ityao/fujin8/src/fujin8')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from btfactory.models import MovieLink

#movies = MovieLink.objects.all()
#movies = MovieLink.objects.filter(images_loaded=False)
movies = MovieLink.objects.filter(images_loaded=False, id__gt=15000, id__lte=20000)
socket.setdefaulttimeout(5)

for movie in movies:
    i = 0
    images = []
    for img in movie.getImages():
        #remote_path = '%s/%s' % ('http://beauty.fujin8.com', img)
        remote_path = img
        month_dir = re.search('/(\d{2}\-\d{2})', movie.daily_link.link).groups()[0]
        ext_name = os.path.splitext(img)[1]
        local_parentpath = '/home/leo/Source/ityao/fujin8/src/fujin8'
        local_filename = '%s_%d%s' % (movie.digestkey, i, ext_name)
        local_relapath = '/media/images/%s/' % (month_dir)
        local_path = '%s%s/%s' % (local_parentpath, local_relapath, local_filename)
        msg = '[%s]%s' % (movie.id, img)
        i += 1
        #if os.path.exists(local_path):
        #    msg = '%s exist.' % msg
        #    print msg
        #else:
        if True:
            if not os.path.exists(os.path.dirname(local_path)):
                os.mkdir(os.path.dirname(local_path))
            try:
                try:
                    filename, header = urllib.urlretrieve(remote_path, local_path)
                except UnicodeError:
                    print(movie.id)
                    exit(-1)
                if 'content-length' in header.keys():
                    msg = '%s %s %s' % (msg, header['Content-Length'], filename)
                    #print '[%s]%s %s' % (movie.id, header['Content-Length'], filename)
                    local_relafilename = '%s%s' % (local_relapath, local_filename)
                    images.append(local_relafilename)
                else:
                    msg = '%s no content length header.' % msg
                print msg
            except socket.timeout:
                print '%s timeout.' % msg
                continue
            except IOError:
                print '%s IO Error.' % msg
                continue

    if images:
        movie.images = ';'.join(images)
        movie.images_loaded = True
        movie.save()
