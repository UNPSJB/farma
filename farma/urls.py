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
from pedidos import views as pviews

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^selectable/', include('selectable.urls')),
    url(r'^$', views.inicio, name="inicio"),
    url(r'^login', views.login_user, name="login"),
    url(r'^logout', views.logout_user, name="logout"),

    # =============================================================================================== #
    #                                       MEDICAMENTOS
    # =============================================================================================== #
    
    # ***************************************** Monodroga *******************************************
    url(r'^monodrogas/$', mviews.monodrogas, name="monodrogas"),
    url(r'^monodrogas/add/$', mviews.monodroga_add, name="monodroga_add"),
    url(r'^monodrogas/update/(?P<id_monodroga>\d+)/$', mviews.monodroga_update, name="monodroga_update"),
    url(r'^monodrogas/delete/(?P<id_monodroga>\d+)/$', mviews.monodroga_delete, name="monodroga_delete"),

    # ************************************** Nombre Fantasia ****************************************
    url(r'^nombresFantasia/$', mviews.nombresFantasia, name="nombresFantasia"),
    url(r'^nombresFantasia/add/$', mviews.nombresFantasia_add, name="nombreFantasia_add"),
    url(r'^nombresFantasia/update/(?P<id_nombreFantasia>\d+)/$', mviews.nombresFantasia_update, name="nombreFantasia_update"),
    url(r'^nombresFantasia/delete/(?P<id_nombreFantasia>\d+)/$', mviews.nombresFantasia_delete, name="nombreFantasia_delete"),


    # *************************************** Presentacion ******************************************
    url(r'^presentaciones/$', mviews.presentaciones, name="presentaciones"),
    url(r'^presentaciones/add/$', mviews.presentacion_add, name="presentacion_add"),
    url(r'^presentaciones/update/(?P<id_presentacion>\d+)/$', mviews.presentacion_update, name="presentacion_update"),
    url(r'^presentaciones/delete/(?P<id_presentacion>\d+)/$', mviews.presentacion_delete, name="presentacion_delete"),

        
    # **************************************** Medicamento ******************************************
    url(r'^medicamentos/$', mviews.medicamentos, name="medicamentos"),
    url(r'^medicamentos/add/$', mviews.medicamento_add, name="medicamento_add"),
    url(r'^medicamentos/update/(?P<id_medicamento>\d+)/$', mviews.medicamento_update, name="medicamento_update"),
    url(r'^medicamentos/delete/(?P<id_medicamento>\d+)/$', mviews.medicamento_delete, name="medicamento_delete"),
    
    
    # =============================================================================================== #
    #                                       ORGANIZACIONES
    # =============================================================================================== #


    # ***************************************** Farmacia *******************************************
    url(r'^farmacias/$', oviews.farmacias, name="farmacias"),
    url(r'^farmacias/add/$', oviews.farmacia_add, name="farmacia_add"),
    url(r'^farmacias/update/(?P<id_farmacia>\d+)/$', oviews.farmacia_update, name="farmacia_update"),
    url(r'^farmacias/delete/(?P<id_farmacia>\d+)/$', oviews.farmacia_delete, name="farmacia_delete"),
    
    
    # ***************************************** Clinica *******************************************
    url(r'^clinicas/$',oviews.clinicas, name="clinicas"),
    url(r'^clinicas/add/$', oviews.clinica_add, name="clinica_add"),
    url(r'^clinicas/update/(?P<id_clinica>\d+)/$', oviews.clinica_update, name="clinica_update"),
    url(r'^clinicas/delete/(?P<id_clinica>\d+)/$', oviews.clinica_delete, name="clinica_delete"),
    

    # *************************************** Laboratorio *****************************************
    url(r'^laboratorios/$',oviews.laboratorios, name="laboratorios"),
    url(r'^laboratorios/add/$', oviews.laboratorio_add, name="laboratorio_add"),
    url(r'^laboratorios/update/(?P<id_laboratorio>\d+)/$', oviews.laboratorio_update, name="laboratorio_update"),
    url(r'^laboratorios/delete/(?P<id_laboratorio>\d+)/$', oviews.laboratorio_delete, name="laboratorio_delete"),
    
    
    # *************************************** Obra Social *****************************************
    url(r'^obrasSociales/$',views.paginaEnConstruccion, name="paginaEnConstruccion"),
    
    
    # =============================================================================================== #
    #                                           PEDIDOS
    # =============================================================================================== #


    # ************************************** Pedido de Farmacia ***************************************
    url(r'^pedidosDeFarmacia/$', pviews.pedidosDeFarmacia, name="pedidosDeFarmacia"),
    url(r'^pedidosDeFarmacia/add/$', pviews.pedidoDeFarmacia_add, name="pedidoDeFarmacia_add"),  
    url(r'^pedidosDeFarmacia/add/registrar-pedido/$', pviews.pedidoDeFarmacia_registrar, name="pedidoDeFarmacia_registrar"),
    url(r'^pedidosDeFarmacia/ver/(?P<id_pedido>\d+)/$', pviews.pedidoDeFarmacia_ver, name="pedidoDeFarmacia_ver"),
    url(r'^pedidosDeFarmacia/add/detalles/$', pviews.detallesPedidoDeFarmacia, name="detallesPedidoDeFarmacia"),
    url(r'^pedidosDeFarmacia/add/detalles/add/$', pviews.detallePedidoDeFarmacia_add, name="detallePedidoDeFarmacia_add"),
    url(r'^pedidosDeFarmacia/add/detalles/update/(?P<id_detalle>\d+)/$', pviews.detallePedidoDeFarmacia_update, name="detallePedidoDeFarmacia_update"),
    url(r'^pedidosDeFarmacia/add/detalles/delete/(?P<id_detalle>\d+)/$', pviews.detallePedidoDeFarmacia_delete, name="detallePedidoDeFarmacia_delete"),
    url(r'^pedidosDeFarmacia/add/detalles/remitoPDF/(?P<id_pedido>\d+)/$', pviews.remitoPDF.as_view(), name="remitoPDF"),


    # ************************************** Pedido de Clinica ***************************************
    url(r'^pedidosDeClinica/$', pviews.pedidosDeClinica, name="pedidosDeClinica"),
    url(r'^pedidosDeClinica/add/$', pviews.pedidoDeClinica_add, name="pedidoDeClinica_add"),
    url(r'^pedidosDeClinica/add/detalles/$', pviews.detallesPedidoDeClinica, name="detallesPedidoDeClinica"),
    url(r'^pedidosDeClinica/add/detalles/add/$', pviews.detallePedidoDeClinica_add, name="detallePedidoDeClinica_add"),
    url(r'^pedidosDeClinica/add/detalles/update/(?P<id_detalle>\d+)/$', pviews.detallePedidoDeClinica_update, name="detallePedidoDeClinica_update"),
    url(r'^pedidosDeClinica/add/detalles/delete/(?P<id_detalle>\d+)/$', pviews.detallePedidoDeClinica_delete, name="detallePedidoDeClinica_delete"),
    url(r'^pedidosDeClinica/add/registrar-pedido/$', pviews.pedidoDeClinica_registrar, name="pedidoDeClinica_registrar"),
    url(r'^pedidosDeClinica/ver/(?P<id_pedido>\d+)/$', pviews.pedidoDeClinica_ver, name="pedidoDeClinica_ver"),

    
    # ************************************** Pedido a Laboratorio ***************************************
    url(r'^pedidosAlaboratorio/$', pviews.pedidosAlaboratorio, name="pedidosAlaboratorio"),
    url(r'^pedidosAlaboratorio/add/$', pviews.pedidoAlaboratorio_add, name="pedidoAlaboratorio_add"),
    url(r'^pedidosAlaboratorio/add/detalles/$', pviews.detallesPedidoAlaboratorio, name="detallesPedidoAlaboratorio"),
    url(r'^pedidosAlaboratorio/add/detalles/add/$', pviews.detallePedidoAlaboratorio_add, name="detallePedidoAlaboratorio_add"),
    url(r'^pedidosAlaboratorio/add/registrar-pedido/$', pviews.pedidoAlaboratorio_registrar, name="pedidoAlaboratorio_registrar"),  
    url(r'^pedidosAlaboratorio/ver/(?P<id_pedido>\d+)/$', pviews.pedidoAlaboratorio_ver, name="pedidoAlaboratorio_ver"),
    
    # ************************************** Recepcion Pedido a Laboratorio ***************************************
    url(r'^recepcionPedidoAlaboratorio/$', pviews.recepcionPedidoAlaboratorio, name="recepcionPedidoAlaboratorio"),
    url(r'^recepcionPedidoAlaboratorio/(?P<id_pedido>\d+)/cargarPedido/$', pviews.recepcionPedidoAlaboratorio_cargarPedido, name="recepcionPedidoAlaboratorio_cargarPedido"),
    url(r'^recepcionPedidoAlaboratorio/(?P<id_pedido>\d+)/controlPedido/$', pviews.recepcionPedidoAlaboratorio_controlPedido, name="recepcionPedidoAlaboratorio_controlPedido"),
    url(r'^recepcionPedidoAlaboratorio/(?P<id_pedido>\d+)/controlPedido/detalle/(?P<id_detalle>\d+)/$', pviews.recepcionPedidoAlaboratorio_controlDetalle, name="recepcionPedidoAlaboratorio_controlDetalle"),
    url(r'^recepcionPedidoAlaboratorio/(?P<id_pedido>\d+)/controlPedido/detalleConNuevoLote/(?P<id_detalle>\d+)/$', pviews.recepcionPedidoAlaboratorio_controlDetalleConNuevoLote, name="recepcionPedidoAlaboratorio_controlDetalleConNuevoLote"),
    url(r'^recepcionPedidoAlaboratorio/(?P<id_pedido>\d+)/controlPedido/registrar/$', pviews.recepcionPedidoAlaboratorio_registrar, name="recepcionPedidoAlaboratorio_registrar"),

      # **************************************** Otros Pedidos ******************************************
    url(r'^devolucionMedicamentosVencidos/$', views.devolucionMedicamentosVencidos,name="devolucionMedicamentosVencidos"),
    url(r'^recepcionReemplazoMedicamentos/$', views.recepcionReemplazoMedicamentos,name="recepcionReemplazoMedicamentos"),
    
      # **************************************** PDFs ******************************************


    # URL'S VIEJAS DE PEDIDO A LABORATORIO
    #    url(r'^pedidoAlaboratorios/verRenglones/(?P<id>\d+)/$', pviews.pedidoAlaboratorios_verRenglones, name="pedidoAlaboratorios_verRenglones"),
    #    url(r'^pedidoAlaboratorios/agregarRenglones/$', pviews.pedidoAlaboratorios_agregarRenglones, name="pedidoAlaboratorios_agregarRenglones"),
    #    url(r'^pedidoAlaboratorios/agregarRenglones/add$', pviews.detallePedidoAlaboratorio_add, name="detallePedidoAlaboratorio_add"),
    #    url(r'^pedidoAlaboratorios/agregarRenglones/registrar-pedido/$', pviews.pedidoAlaboratorio_registrar, name="pedidoAlaboratorio_registrar"),
    #    url(r'^ListPedidoAlaboratorio/$', pviews.ListPedidoALaboratorio, name="ListPedidoALaboratorio"),
    #    url(r'^pedidoAlaboratorios/add/$', pviews.PedidoLaboratorio_add, name="PedidoLaboratorio_add"),

]
