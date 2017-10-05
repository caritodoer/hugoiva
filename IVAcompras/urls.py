from django.conf.urls import url
from django.contrib import admin
from . import views

#a=alta
#m=modificar
#v=ver detalle
#l=listado
#d=delete

urlpatterns = [
	url(r'^$', views.home, name='home'),
	# empresa

	url(r'^a_empresa/$', views.a_empresa, name='a_empresa'),
	url(r'^m_empresa/(?P<id>\d+)/$', views.m_empresa, name='m_empresa'),
	url(r'^v_empresa/(?P<id>\d+)/$', views.v_empresa, name='v_empresa'),
	url(r'^d_empresa/(?P<id>\d+)/$', views.d_empresa, name='d_empresa'),

	# cliente_proveedor

	url(r'^a_cli_pro/$', views.a_cli_pro, name='a_cli_pro'),
	url(r'^m_cli_pro/(?P<id>\d+)/$', views.m_cli_pro),
	url(r'^v_cli_pro/(?P<id>\d+)/$', views.v_cli_pro, name='v_cli_pro'),
	url(r'^d_cli_pro/(?P<id>\d+)/$', views.d_cli_pro),

	# Libro

	url(r'^a_libro/(?P<k>[^/]+)/(?P<v>[^/]+)/$', views.a_libro, name='a_libro'),
	url(r'^m_libro/(?P<id>\d+)/$', views.m_libro),
	url(r'^v_libro/(?P<id>\d+)/$', views.v_libro, name='v_libro'),
	url(r'^d_libro/(?P<id>\d+)/$', views.d_libro),
	url(r'^l_libro/$', views.l_libro, name='l_libro'),

	# Detalle

	url(r'^a_detalle/$', views.a_detalle, name='a_detalle'),
	url(r'^m_detalle/(?P<id>\d+)/$', views.m_detalle),
	url(r'^v_detalle/(?P<id>\d+)/$', views.v_detalle, name='v_detalle'),
	url(r'^d_detalle/(?P<id>\d+)/$', views.d_detalle),
	url(r'^l_detalle/$', views.l_detalle, name='l_detalle'),

]