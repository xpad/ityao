#!/home/leo/Source/ldap_env/bin/python
import os
import os.path
import sys
import urllib

sys.path.append('/home/leo/Source/ldap_env')
sys.path.append('/home/leo/Source/ityao/fujin8/src/fujin8')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from btfactory.models import MovieLink

movies = MovieLink.objects.all()

for movie in movies:
    for img in movie.getImages():
        remote_path = '%s/%s' % ('http://beauty.fujin8.com', img)
        locate_path = '%s/%s' % ('/home/leo/Source/ityao/fujin8/src/fujin8', img)
        if os.path.exists(locate_path):
            print '[%s]%s exist.' % (movie.id, img)
        else:
            filename, header = urllib.urlretrieve(remote_path, locate_path)
            print '[%s]%s %s' % (movie.id, header['Content-Length'], filename)
