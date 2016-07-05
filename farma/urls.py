from django.conf.urls import include, url
from django.contrib import admin
from . import views
from medicamentos import views as mviews
from organizaciones import views as oviews
from pedidos import views as pviews
from usuarios import views as uviews

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^selectable/', include('selectable.urls')),
    url(r'^$', views.inicio, name="inicio"),

    # =============================================================================================== #
    #                                       USUARIOS
    # =============================================================================================== #
    url(r'^login', uviews.login_user, name="login"),
    url(r'^logout', uviews.logout_user, name="logout"),
    url(r'^perfil/addUsuario/$', uviews.usuario_add, name="usuario_add"),

    # =============================================================================================== #
    #                                       MEDICAMENTOS
    # =============================================================================================== #
    
    # ***************************************** Monodroga *******************************************
    url(r'^monodrogas/$', mviews.monodrogas, name="monodrogas"),
    url(r'^monodrogas/add/$', mviews.monodroga_add, name="monodroga_add"),
    url(r'^monodrogas/update/(?P<id_monodroga>\d+)/$', mviews.monodroga_update, name="monodroga_update"),
    url(r'^monodrogas/tryDelete/(?P<id_monodroga>\d+)/$', mviews.monodroga_try_delete, name="monodroga_try_delete"),
    url(r'^monodrogas/delete/(?P<id_monodroga>\d+)/$', mviews.monodroga_delete, name="monodroga_delete"),

    # ************************************** Nombre Fantasia ****************************************
    url(r'^nombresFantasia/$', mviews.nombresFantasia, name="nombresFantasia"),
    url(r'^nombresFantasia/add/$', mviews.nombresFantasia_add, name="nombreFantasia_add"),
    url(r'^nombresFantasia/update/(?P<id_nombreFantasia>\d+)/$', mviews.nombresFantasia_update, name="nombreFantasia_update"),
    url(r'^nombresFantasia/tryDelete/(?P<id_nombreFantasia>\d+)/$', mviews.nombresFantasia_try_delete, name="nombreFantasia_try_delete"),
    url(r'^nombresFantasia/delete/(?P<id_nombreFantasia>\d+)/$', mviews.nombresFantasia_delete, name="nombreFantasia_delete"),

    # *************************************** Presentacion ******************************************
    url(r'^presentaciones/$', mviews.presentaciones, name="presentaciones"),
    url(r'^presentaciones/add/$', mviews.presentacion_add, name="presentacion_add"),
    url(r'^presentaciones/update/(?P<id_presentacion>\d+)/$', mviews.presentacion_update, name="presentacion_update"),
    url(r'^presentaciones/tryDelete/(?P<id_presentacion>\d+)/$', mviews.presentacion_try_delete, name="presentacion_try_delete"),
    url(r'^presentaciones/delete/(?P<id_presentacion>\d+)/$', mviews.presentacion_delete, name="presentacion_delete"),

    # **************************************** Medicamento ******************************************
    url(r'^medicamentos/$', mviews.medicamentos, name="medicamentos"),
    url(r'^medicamentos/add/$', mviews.medicamento_add, name="medicamento_add"),
    url(r'^medicamentos/updateStockMinimo/(?P<id_medicamento>\d+)/$', mviews.medicamento_updateStockMinimo, name="medicamento_update_stock_minimo"),
    url(r'^medicamentos/updatePrecioVenta/(?P<id_medicamento>\d+)/$', mviews.medicamento_updatePrecioVenta, name="medicamento_update_precio_venta"),
    url(r'^medicamentos/delete/(?P<id_medicamento>\d+)/$', mviews.medicamento_delete, name="medicamento_delete"),
    url(r'^medicamentos/tryDelete/(?P<id_medicamento>\d+)/$', mviews.medicamento_try_delete, name="medicamento_try_delete"),
    url(r'^medicamentos/verLotes/(?P<id_medicamento>\d+)/$', mviews.medicamento_verLotes, name="medicamento_verLotes"),
    url(r'^medicamentos/estadisticas/topPorCantidad/$', mviews.medicamentos_topPorCantidad, name="medicamentos_topPorCantidad"),
    url(r'^medicamentos/estadisticas/topPorCantidad/downloadExcel/$', mviews.medicamentos_topPorCantidadExcel, name="medicamentos_topPorCantidadExcel"),
    url(r'^medicamentos/estadisticas/topPorPedido/$', mviews.medicamentos_topPorPedido, name="medicamentos_topPorPedido"),
    url(r'^medicamentos/estadisticas/topPorPedido/downloadExcel/$', mviews.medicamentos_topPorPedidoExcel, name="medicamentos_topPorPedidoExcel"),
    url(r'^medicamentos/estadisticas/topOrganizacionesPorCantidad/$', mviews.medicamentos_topOrganizacionesPorCantidad, name="medicamentos_topOrganizacionesPorCantidad"),
    url(r'^medicamentos/estadisticas/topOrganizacionesPorCantidad/downloadExcel/$', mviews.medicamentos_topOrganizacionesPorCantidadExcel, name="medicamentos_topOrganizacionesPorCantidadExcel"),
    url(r'^medicamentos/estadisticas/topOrganizacionesPorPedidos/$', mviews.medicamentos_topOrganizacionesPorPedidos, name="medicamentos_topOrganizacionesPorPedidos"),
url(r'^medicamentos/estadisticas/topOrganizacionesPorPedido/downloadExcel/$', mviews.medicamentos_topOrganizacionesPorPedidoExcel, name="medicamentos_topOrganizacionesPorPedidoExcel"),

    # =============================================================================================== #
    #                                       ORGANIZACIONES
    # =============================================================================================== #

    # ***************************************** Farmacia *******************************************
    url(r'^farmacias/$', oviews.farmacias, name="farmacias"),
    url(r'^farmacias/add/$', oviews.farmacia_add, name="farmacia_add"),
    url(r'^farmacias/update/(?P<id_farmacia>\d+)/$', oviews.farmacia_update, name="farmacia_update"),
    url(r'^farmacias/tryDelete/(?P<id_farmacia>\d+)/$', oviews.farmacia_try_delete, name="farmacia_try_delete"),
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
    url(r'^laboratorios/tryDelete/(?P<id_laboratorio>\d+)/$', oviews.laboratorio_try_delete, name="laboratorio_try_delete"),
    url(r'^laboratorios/delete/(?P<id_laboratorio>\d+)/$', oviews.laboratorio_delete, name="laboratorio_delete"),

    # *************************************** Obra Social *****************************************
    url(r'^obrasSociales/$', views.paginaEnConstruccion, name="paginaEnConstruccion"),

    # =============================================================================================== #
    #                                           PEDIDOS
    # =============================================================================================== #

    # ************************************** Pedido de Farmacia ***************************************
    url(r'^pedidosDeFarmacia/$', pviews.pedidosDeFarmacia, name="pedidosDeFarmacia"),
    url(r'^pedidosDeFarmacia/add/$', pviews.pedidoDeFarmacia_add, name="pedidoDeFarmacia_add"),  
    url(r'^pedidosDeFarmacia/add/registrar-pedido/$', pviews.pedidoDeFarmacia_registrar, name="pedidoDeFarmacia_registrar"),
    url(r'^pedidosDeFarmacia/ver/(?P<id_pedido>\d+)/$', pviews.pedidoDeFarmacia_ver, name="pedidoDeFarmacia_ver"),
    url(r'^pedidosDeFarmacia/verDetalles/(?P<id_pedido>\d+)/$', pviews.pedidoDeFarmacia_verDetalles, name="pedidoDeFarmacia_verDetalles"),
    url(r'^pedidosDeFarmacia/verRemitos/(?P<id_pedido>\d+)/$', pviews.pedidoDeFarmacia_verRemitos, name="pedidoDeFarmacia_verRemitos"),
    url(r'^pedidosDeFarmacia/add/detalles/$', pviews.detallesPedidoDeFarmacia, name="detallesPedidoDeFarmacia"),
    url(r'^pedidosDeFarmacia/add/detalles/add/$', pviews.detallePedidoDeFarmacia_add, name="detallePedidoDeFarmacia_add"),
    url(r'^pedidosDeFarmacia/add/detalles/update/(?P<id_detalle>\d+)/$', pviews.detallePedidoDeFarmacia_update, name="detallePedidoDeFarmacia_update"),
    url(r'^pedidosDeFarmacia/add/detalles/delete/(?P<id_detalle>\d+)/$', pviews.detallePedidoDeFarmacia_delete, name="detallePedidoDeFarmacia_delete"),
    url(r'^pedidosDeFarmacia/remitoDeFarmacia/(?P<id_remito>\d+)/$', pviews.remitoDeFarmacia.as_view(), name="remitoDeFarmacia"),
    url(r'^pedidosDeFarmacia/estadisticas/topPorCantidadMedicamentos/$', pviews.pedidosDeFarmacia_topFarmaciasConMasMedicamentos, name="pedidosDeFarmacia_topFarmaciasConMasMedicamentos"),
    url(r'^pedidosDeFarmacia/estadisticas/topPorCantidadMedicamentos/downloadExcel/$', pviews.pedidosDeFarmacia_topFarmaciasConMasMedicamentosExcel, name="pedidosDeFarmacia_topFarmaciasConMasMedicamentosExcel"),
    url(r'^pedidosDeFarmacia/estadisticas/topPorCantidadPedidos/$', pviews.pedidosDeFarmacia_topFarmaciasConMasPedidos, name="pedidosDeFarmacia_topFarmaciasConMasPedidos"),
    url(r'^pedidosDeFarmacia/estadisticas/topPorCantidadPedidos/downloadExcel/$', pviews.pedidosDeFarmacia_topFarmaciasConMasPedidosExcel, name="pedidosDeFarmacia_topFarmaciasConMasPedidosExcel"),


    # ************************************** Pedido de Clinica ***************************************
    url(r'^pedidosDeClinica/$', pviews.pedidosDeClinica, name="pedidosDeClinica"),
    url(r'^pedidosDeClinica/add/$', pviews.pedidoDeClinica_add, name="pedidoDeClinica_add"),
    url(r'^pedidosDeClinica/add/detalles/$', pviews.detallesPedidoDeClinica, name="detallesPedidoDeClinica"),
    url(r'^pedidosDeClinica/add/detalles/add/$', pviews.detallePedidoDeClinica_add, name="detallePedidoDeClinica_add"),
    url(r'^pedidosDeClinica/add/detalles/update/(?P<id_detalle>\d+)/$', pviews.detallePedidoDeClinica_update, name="detallePedidoDeClinica_update"),
    url(r'^pedidosDeClinica/add/detalles/delete/(?P<id_detalle>\d+)/$', pviews.detallePedidoDeClinica_delete, name="detallePedidoDeClinica_delete"),
    url(r'^pedidosDeClinica/add/registrar-pedido/$', pviews.pedidoDeClinica_registrar, name="pedidoDeClinica_registrar"),
    url(r'^pedidosDeClinica/ver/(?P<id_pedido>\d+)/$', pviews.pedidoDeClinica_ver, name="pedidoDeClinica_ver"),
    url(r'^pedidosDeClinica/verDetalles/(?P<id_pedido>\d+)/$', pviews.pedidoDeClinica_verDetalles, name="pedidoDeClinica_verDetalles"),
    url(r'^pedidosDeClinica/verRemitos/(?P<id_pedido>\d+)/$', pviews.pedidoDeClinica_verRemitos, name="pedidoDeClinica_verRemitos"),
    url(r'^pedidosDeClinica/remitoDeClinica/(?P<id_remito>\d+)/$', pviews.remitoDeClinica.as_view(), name="remitoDeClinica"),
    url(r'^pedidosDeClinica/estadisticas/topPorCantidadMedicamentos/$', pviews.pedidosDeClinica_topClinicasConMasMedicamentos, name="pedidosDeClinica_topClinicasConMasMedicamentos"),
    url(r'^pedidosDeClinica/estadisticas/topPorCantidadMedicamentos/downloadExcel/$', pviews.pedidosDeClinica_topClinicasConMasMedicamentosExcel, name="pedidosDeClinica_topClinicasConMasMedicamentosExcel"),
    url(r'^pedidosDeClinica/estadisticas/topPorCantidadPedidos/$', pviews.pedidosDeClinica_topClinicasConMasPedidos, name="pedidosDeClinica_topClinicasConMasPedidos"),
    url(r'^pedidosDeClinica/estadisticas/topPorCantidadPedidos/downloadExcel/$', pviews.pedidosDeClinica_topClinicasConMasPedidosExcel, name="pedidosDeClinica_topClinicasConMasPedidosExcel"),

    url(r'^getObrasSociales/(?P<id_clinica>\d+)/$', pviews.get_obrasSociales, name="get_obrasSociales"),    

    # ************************************** Pedido a Laboratorio ***************************************
    url(r'^pedidosAlaboratorio/$', pviews.pedidosAlaboratorio, name="pedidosAlaboratorio"),
    url(r'^pedidosAlaboratorio/add/$', pviews.pedidoAlaboratorio_add, name="pedidoAlaboratorio_add"),
    url(r'^pedidosAlaboratorio/add/detalles/$', pviews.detallesPedidoAlaboratorio, name="detallesPedidoAlaboratorio"),
    url(r'^pedidosAlaboratorio/add/detalles/add/$', pviews.detallePedidoAlaboratorio_add, name="detallePedidoAlaboratorio_add"),
    url(r'^pedidosAlaboratorio/add/detalles/update/(?P<id_detalle>\d+)/$', pviews.detallePedidoAlaboratorio_update, name="detallePedidoAlaboratorio_update"),
    url(r'^pedidosAlaboratorio/add/detalles/delete/(?P<id_detalle>\d+)/$', pviews.detallePedidoAlaboratorio_delete, name="detallePedidoAlaboratorio_delete"),
    url(r'^pedidosAlaboratorio/add/registrar-pedido/$', pviews.pedidoAlaboratorio_registrar, name="pedidoAlaboratorio_registrar"),
    url(r'^pedidosAlaboratorio/cancelar/(?P<id_pedido>\d+)/$', pviews.pedidoAlaboratorio_cancelar, name="pedidoAlaboratorio_cancelar"), 
    url(r'^pedidosAlaboratorio/verDetalles/(?P<id_pedido>\d+)/$', pviews.pedidoAlaboratorio_verDetalles, name="pedidoAlaboratorio_verDetalles"), 
    url(r'^pedidosAlaboratorio/verRemitos/(?P<id_pedido>\d+)/$', pviews.pedidoAlaboratorio_verRemitos, name="pedidoAlaboratorio_verRemitos"),
    url(r'^pedidosAlaboratorio/ver/(?P<id_pedido>\d+)/$', pviews.pedidoAlaboratorio_ver, name="pedidoAlaboratorio_ver"),
    url(r'^pedidosAlaboratorio/remitoDeLaboratorio/(?P<id_remito>\d+)/$', pviews.remitoDeLaboratorio.as_view(), name="remitoDeLaboratorio"),
    url(r'^pedidosAlaboratorio/estadisticas/topPorSolicitudMedicamentos/$', pviews.pedidosAlaboratorio_topLabConMasSolicitudesMedicamentos, name="pedidosAlaboratorio_topLabConMasSolicitudesMedicamentos"),
    url(r'^pedidosAlaboratorio/estadisticas/topPorSolicitudMedicamentos/downloadExcel/$', pviews.pedidosAlaboratorio_topLabConMasSolicitudesMedicamentosExcel, name="pedidosAlaboratorio_topLabConMasSolicitudesMedicamentosExcel"),
    url(r'^pedidosAlaboratorio/estadisticas/topPorSolicitudPedidos/$', pviews.pedidosAlaboratorio_topLabConMasSolicitudesPedidos, name="pedidosAlaboratorio_topLabConMasSolicitudesPedidos"),
    url(r'^pedidosAlaboratorio/estadisticas/topPorSolicitudPedidos/downloadExcel/$', pviews.pedidosAlaboratorio_topLabConMasSolicitudesPedidosExcel, name="pedidosAlaboratorio_topLabConMasSolicitudesPedidosExcel"),


    # ************************************** Recepcion Pedido a Laboratorio ***************************************
    url(r'^recepcionPedidoAlaboratorio/$', pviews.recepcionPedidoAlaboratorio, name="recepcionPedidoAlaboratorio"),
    url(r'^recepcionPedidoAlaboratorio/(?P<id_pedido>\d+)/registrar/$',pviews.recepcionPedidoAlaboratorio_registrarRecepcion, name="recepcionPedidoAlaboratorio_registrarRecepcion"),
    url(r'^recepcionPedidoAlaboratorio/(?P<id_pedido>\d+)/cargarPedido/$', pviews.recepcionPedidoAlaboratorio_cargarPedido, name="recepcionPedidoAlaboratorio_cargarPedido"),
    url(r'^recepcionPedidoAlaboratorio/(?P<id_pedido>\d+)/controlPedido/$', pviews.recepcionPedidoAlaboratorio_controlPedido, name="recepcionPedidoAlaboratorio_controlPedido"),
    url(r'^recepcionPedidoAlaboratorio/(?P<id_pedido>\d+)/controlPedido/detalle/(?P<id_detalle>\d+)/$', pviews.recepcionPedidoAlaboratorio_controlDetalle, name="recepcionPedidoAlaboratorio_controlDetalle"),
    url(r'^recepcionPedidoAlaboratorio/(?P<id_pedido>\d+)/controlPedido/detalleConNuevoLote/(?P<id_detalle>\d+)/$', pviews.recepcionPedidoAlaboratorio_controlDetalleConNuevoLote, name="recepcionPedidoAlaboratorio_controlDetalleConNuevoLote"),
    url(r'^recepcionPedidoAlaboratorio/(?P<id_pedido>\d+)/controlPedido/registrar/$', pviews.recepcionPedidoAlaboratorio_registrar, name="recepcionPedidoAlaboratorio_registrar"),

    # **************************************** Otros Pedidos ******************************************
    url(r'^devolucionMedicamentosVencidos/$', pviews.devolucionMedicamentosVencidos, name="devolucionMedicamentosVencidos"),
    url(r'^devolucionMedicamentosVencidos/detalles/(?P<id_laboratorio>\d+)/$', pviews.devolucionMedicamentosVencidos_detalle, name="devolucionMedicamentosVencidos_detalle"),
    url(r'^devolucionMedicamentosVencidos/detalles/(?P<id_laboratorio>\d+)/registar/$', pviews.devolucionMedicamentosVencidos_registrar, name="devolucionMedicamentosVencidos_registrar"),
    url(r'^devolucionMedicamentosVencidos/remitoDevolucion/(?P<id_remito>\d+)/$', pviews.remitoDevolucion.as_view(), name="remitoDevolucion"),
]