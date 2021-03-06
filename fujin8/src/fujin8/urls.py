from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^index.html', 'fujin8.views.home', name='home'),
    url(r'^about.html', 'fujin8.views.about', name='about'),
    url(r'^$', 'fujin8.views.home', name='home'),
    (r'^time$', 'fujin8.views.home'), 
    (r'^time/json$', 'fujin8.views.timestamp'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^btfactory/', include('fujin8.btfactory.urls')),
    #url(r'^accounts/', include('registration.backends.default.urls')),  
    url(r'^accounts/', include('registration.urls')),  
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

