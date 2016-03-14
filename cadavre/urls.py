from django.conf.urls import url, patterns
from . import views

urlpatterns = patterns('cadavre.views',
	url(r'^home$', 'home'),
	url(r'^disconnect$', 'logout_page'),
	url(r'^confirm/(?P<activation_key>\w+)/', 'register_confirm'),
	url(r'^email_pass$', 'email_reset_pass'),
	url(r'^reset/(?P<activation_key>\w+)/', 'reset_pass'),
	url(r'^home_cadavre$', 'home_cadavre'),
	url(r'^confirm_cadavre$', 'confirm_cadavre'),
	url(r'^confirm_sentance$', 'confirm_sentance'),
	url(r'^explorer$', 'explorer'),
	url(r'^account$', 'account'),
	url(r'^rules$', 'rules'),
	
	url(r'^(?P<username>\w+)$', 'profil'),

)

