from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('project.apps.lotto.views',
    url(r'^$', 'index', name='index'),
    
    # user
    url(r'^register$', 'register', name='register'),
    url(r'^login$', 'user_login', name='login'),
    url(r'^logout$', 'user_logout', name='logout'),
    
    # tickets
    url(r'^ticket/create$', 'ticket_create', name='ticket_create'),
    url(r'^ticket/edit/(?P<ticket_id>\d+)/$', 'ticket_edit', name='ticket_edit'),
    url(r'^ticket/delete/(?P<ticket_id>\d+)/$', 'ticket_delete',
        name='ticket_delete'),
    url(r'^ticket/list$', 'ticket_list', name='ticket_list'),
    url(r'^ticket/list-upcoming$', 'ticket_list_upcoming',
        name='ticket_list_upcoming'),
    url(r'^ticket/check$', 'ticket_check', name='ticket_check'),
    
    #ajax
    url(r'^ticket/ajax/check$', 'ticket_ajax_check', name='ticket_ajax_check'),
    
) + staticfiles_urlpatterns()

