from django.conf.urls import url
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
	url(r'^$', index, name='index'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='rpg/login.html', redirect_authenticated_user=True), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='rpg/logout.html'), name='logout'),
	url(r'^battle/$', battle, name='battle'),
	url(r'^monsterbook/$', monsterbook, name='monsterbook'),
	url(r'^skillbook/$', skillbook, name='skillbook'),
]
