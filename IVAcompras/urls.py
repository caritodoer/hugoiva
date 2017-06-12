from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
# Proveedores

url(r'^a_proveedor/$', views.a_proveedor),
url(r'^m_proveedor/(?P<id>\d+)/$', views.m_proveedor),
url(r'^v_proveedor/(?P<id>\d+)/$', views.v_proveedor, name='d_proveedor'),



# Clientes

url(r'^a_cliente/$', views.a_cliente),
url(r'^m_cliente/(?P<id>\d+)/$', views.m_cliente),
url(r'^v_cliente/(?P<id>\d+)/$', views.v_cliente, name='d_cliente'),

# Libro

url(r'^a_libro/$', views.a_libro),
url(r'^m_libro/(?P<id>\d+)/$', views.m_libro),
url(r'^v_libro/(?P<id>\d+)/$', views.v_libro, name='d_libro'),

]