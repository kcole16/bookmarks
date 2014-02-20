from django.conf.urls import patterns, url
from bookmarks import views


urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^add_list/$', views.add_list, name='add_list'),
	url(r'^list/(?P<list_name_url>\w+)/$', views.list, name='lists'),
	url(r'^list/(?P<list_name_url>\w+)/add_link/$', views.add_link, name='add_link'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	#url(r'^delete_link/(?P<link_to_delete>[0-9]+)/$', views.delete_link, name='delete_link')
	url(r'^delete_link/(?P<link_id>\w+)/$', views.delete_link, name='delete_link'),
	)

