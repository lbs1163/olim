from django.conf.urls import url
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^$', index, name='index'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='rpg/login.html', redirect_authenticated_user=True), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='rpg/logout.html'), name='logout'),
	url(r'^combination/$', combination, name='combination'),
	url(r'^map/$', map, name='map'),
	url(r'^battle/$', battle, name='battle'),
	url(r'^bossbattle/$', bossbattle, name='bossbattle'),
	url(r'^monsterbook/$', monsterbook, name='monsterbook'),
	url(r'^skillbook/$', skillbook, name='skillbook'),
	url(r'^selectskill/$', selectskill, name='selectskill'),
	url(r'^finalbossbattle/$', finalbossbattle, name='finalbossbattle'),
	url(r'^ending/$', ending, name='ending'),
	url(r'^reward/$', reward, name='reward'),
	url(r'^custom/$', custom, name='custom'),
	url(r'^code/$', code, name='code'),
	url(r'^codemenu/$', codemenu, name='codemenu'),
	url(r'^day1/$', day1, name='day1'),
	url(r'^day2/$', day2, name='day2'),
	url(r'^day3/$', day3, name='day3'),
	url(r'^day4/$', day4, name='day4'),
	url(r'^all/$', all, name='all'),
]
