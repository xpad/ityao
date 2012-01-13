#!/home/leo/Source/ldap_env/bin/python
import os
import os.path
import sys
import urllib2
import hashlib
import socket

sys.path.append('/home/leo/Source/ldap_env')
sys.path.append('/home/leo/Source/ityao/fujin8/src')
sys.path.append('/home/leo/Source/ityao/fujin8/src/fujin8')
os.environ['DJANGO_SETTINGS_MODULE'] = 'fujin8.settings'

from fujin8.btfactory.models import MonthlyLink, DailyLink, MovieLink

movies = MovieLink.objects.all()
