"""organizandor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from medicamentos import views as mviews
from organizaciones import views as oviews

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.inicio, name="inicio"),
    url(r'^login', views.login_user, name="login"),
    url(r'^logout', views.logout_user, name="logout"),

    # ****** MEDICAMENTOS ******
    url(r'^monodrogas/$', mviews.monodrogas, name="monodrogas"),
    url(r'^monodrogas/add/$', mviews.monodrogas, name="monodroga_add"),
    url(r'^altaMedicamento/$', views.altaMedicamento, name="altaMedicamento"),
    url(r'^nombresFantasia/$', mviews.nombresFantasia, name="nombresFantasia"),
    url(r'^nombresFantasia_add/$', mviews.nombresFantasia, name="nombresFantasia_add"),
    url(r'^Presentacion/$', mviews.presentacion, name="presentacion"),
    url(r'^Presentacion_add/$', mviews.presentacion, name="presentacion_add"),

    # ****** PEDIDOS ******
    url(r'^pedidoALaboratorio/$', views.pedidoALaboratorio, name="pedidoALaboratorio"),
    url(r'^recepcionPedidoDeLaboratorio/$', views.recepcionPedidoDeLaboratorio, name="recepcionPedidoDeLaboratorio"),
    url(r'^pedidoDeFarmacia/$', views.pedidoDeFarmacia, name="pedidoDeFarmacia"),
    url(r'^pedidoDeClinica/$', views.pedidoDeClinica,name="pedidoDeClinica"),
    url(r'^devolucionMedicamentosVencidos/$', views.devolucionMedicamentosVencidos,name="devolucionMedicamentosVencidos"),
    url(r'^recepcionReemplazoMedicamentos/$', views.recepcionReemplazoMedicamentos,name="recepcionReemplazoMedicamentos"),
    
    # ****** FARMACIAS ******
    url(r'^farmacias/$',oviews.farmacias, name="farmacias"),
    url(r'^farmacias/add/$', oviews.farmacia_add, name="farmacia_add"),
    url(r'^farmacias/modify/(?P<pk>\d+)/$', oviews.farmacias, name="farmacia_modify"),
    url(r'^farmacias/delete/(?P<pk>\d+)/$', oviews.farmacia_delete, name="farmacia_delete"),
    
    
    # ****** CLINICAS ******
    url(r'^clinicas/$',oviews.clinicas, name="clinicas"),
    url(r'^clinicas/add/$', oviews.clinica_add, name="clinica_add"),
    url(r'^clinicas/modify/(?P<pk>\d+)/$', oviews.clinicas, name="clinica_modify"),
    url(r'^clinicas/delete/(?P<pk>\d+)/$', oviews.clinica_delete, name="clinica_delete"),
    

    # ****** LABORATORIOS ******
    url(r'^laboratorios/$',oviews.laboratorios, name="laboratorios"),
    url(r'^laboratorios/add/$', oviews.laboratorio_add, name="laboratorio_add"),
    url(r'^laboratorios/modify/(?P<pk>\d+)/$', oviews.laboratorios, name="laboratorio_modify"),
    url(r'^laboratorios/delete/(?P<pk>\d+)/$', oviews.laboratorio_delete, name="laboratorio_delete"),
    
    
    # ****** OTROS ******
    url(r'^error404/$',views.error404, name="error404"),
]
