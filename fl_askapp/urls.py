from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<page>\d+)/', views.index, name='index'),

	url(r'^developing/', views.developing, name='developing'),

	url(r'^hot/(?P<page>\d+)/', views.hot_questions, name='hot_questions'),
	url(r'^hot/', views.hot_questions, name='hot_questions'),

	url(r'^question/id(?P<id>\d+)/(?P<page>\d+)?/$', views.single_question, name='question'),
	url(r'^question/id(?P<id>\d+)/$', views.single_question, name='question'),
    url(r'^edit/question/id(?P<id>\d+)/$', views.edit_question, name='edit_question'),

	url(r'^ask/', views.ask_question, name='ask'),
	url(r'^login/', views.login, name='login'),
    url(r'^logout/?$', views.logout, name='logout'),
	url(r'^signup/', views.signup, name='signup'),
    url(r'^change_password/', views.change_password, name='change_password'),

	url(r'^tag/(?P<tag>(\d|\w|[-+_.:;~&@*%#$])+)/$', views.tag, name='tag'),
	url(r'^tag/(?P<tag>(\d|\w|[-+_.:;~&@*%#$])+)/(?P<page>\d+)/$', views.tag, name='tag'),

	url(r'^profile/(?P<user_name>\w+)/(?P<page>\d+)?/$', views.profile, name='profile'),
	url(r'^profile/(?P<user_name>\w+)/$', views.profile, name='profile'),
    url(r'^edit/profile/$', views.profile_edit, name='profile_edit'),

	url(r'^get_prms', views.get_prms, name='get_prms'),
]
