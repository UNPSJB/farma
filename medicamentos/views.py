from django.shortcuts import render, redirect, get_object_or_404
from . import models, forms, utils
from django.contrib.auth.decorators import login_required
from jsonview.decorators import json_view
from django.contrib.auth.decorators import permission_required
from pedidos.views import get_filtros as get_filtros_pedidos
from pedidos import models as pmodels
from django.http import HttpResponse
import json
from xlsxwriter import Workbook
import io


def get_filtros(get, modelo):
    mfilter = {}
    for filtro in modelo.FILTROS:
        attr = filtro.split("__")[0]
        if attr in get and get[attr]:
            mfilter[filtro] = get[attr]
            mfilter[attr] = get[attr]
    return mfilter


def hubo_alta(session):
    if 'successAdd' in session:
        del session['successAdd']
        return True
    return False


def clone_query(query):
    clone = {}
    for key, val in query.items():
        if val:
            clone[key] = val
    return clone


@login_required(login_url='login')
def monodrogas(request):
    filters = get_filtros(request.GET, models.Monodroga)
    mfilters = dict(filter(lambda v: v[0] in models.Monodroga.FILTROS, filters.items()))
    monodrogas = models.Monodroga.objects.filter(**mfilters)
    estadisticas = {
        'total': models.Monodroga.objects.all().count(),
        'filtrados': monodrogas.count()
    }
    return render(request, "monodroga/monodrogas.html", {"monodrogas": monodrogas, "filtros": filters, 'estadisticas': estadisticas})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def monodroga_add(request):
    if request.method == "POST":
        form = forms.MonodrogaFormAdd(request.POST)
        if form.is_valid():
            form.save()
            if '_volver' in request.POST:
                return redirect('monodrogas')
            else:
                request.session['successAdd'] = True
                return redirect('monodroga_add')
    else:
        form = forms.MonodrogaFormAdd()
    successAdd = hubo_alta(request.session)
    return render(request, "monodroga/monodrogaAdd.html", {"form": form, 'successAdd': successAdd})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def monodroga_update(request, id_monodroga):
    monodroga = get_object_or_404(models.Monodroga, pk=id_monodroga)
    if request.method == "POST":
        form = forms.MonodrogaFormUpdate(request.POST, instance=monodroga)
        if form.is_valid():
            form.save()
            return redirect('monodrogas')
    else:
        form = forms.MonodrogaFormUpdate(instance=monodroga)
    return render(request, "monodroga/monodrogaUpdate.html", {'form': form, 'monodroga': monodroga})


@json_view
@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def monodroga_try_delete(request, id_monodroga):
    infoBaja = utils.puedo_eliminar_monodroga(id_monodroga)
    return infoBaja


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def monodroga_delete(request, id_monodroga):
    infoBaja = utils.puedo_eliminar_monodroga(id_monodroga)
    if infoBaja['success']:
        monodroga = models.Monodroga.objects.get(pk=id_monodroga)
        monodroga.delete()
        return redirect('monodrogas')


@login_required(login_url='login')
def nombresFantasia(request):
    filters = get_filtros(request.GET, models.NombreFantasia)
    mfilters = dict(filter(lambda v: v[0] in models.NombreFantasia.FILTROS, filters.items()))
    nombresFantasia = models.NombreFantasia.objects.filter(**mfilters)
    estadisticas = {
        'total': models.NombreFantasia.objects.all().count(),
        'filtrados': nombresFantasia.count()
    }
    return render(request, "nombreFantasia/nombresFantasia.html", {"nombresFantasia": nombresFantasia, "filtros": filters, 'estadisticas': estadisticas})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def nombresFantasia_add(request):
    if request.method == "POST":
        form = forms.NombreFantasiaFormAdd(request.POST)
        if form.is_valid():
            form.save()
            if '_volver' in request.POST:
                return redirect('nombresFantasia')
            else:
                request.session['successAdd'] = True
                return redirect('nombreFantasia_add')
    else:
        form = forms.NombreFantasiaFormAdd()
    successAdd = hubo_alta(request.session)
    return render(request, "nombreFantasia/nombreFantasiaAdd.html", {"form": form, 'successAdd': successAdd})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def nombresFantasia_update(request, id_nombreFantasia):
    nombreFantasia = get_object_or_404(models.NombreFantasia, pk=id_nombreFantasia)
    if request.method == "POST":
        form = forms.NombreFantasiaFormUpdate(request.POST, instance=nombreFantasia)
        if form.is_valid():
            form.save()
            return redirect('nombresFantasia')
    else:
        form = forms.NombreFantasiaFormUpdate(instance=nombreFantasia)
    return render(request, "nombreFantasia/nombreFantasiaUpdate.html", {'form': form, 'nombreFantasia': nombreFantasia})


@json_view
@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def nombresFantasia_try_delete(request, id_nombreFantasia):
    infoBaja = utils.puedo_eliminar_nombreFantasia(id_nombreFantasia)
    return infoBaja


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def nombresFantasia_delete(request, id_nombreFantasia):
    infoBaja = utils.puedo_eliminar_nombreFantasia(id_nombreFantasia)
    if infoBaja['success']:
        nombreFantasia = models.NombreFantasia.objects.get(pk=id_nombreFantasia)
        nombreFantasia.delete()
        return redirect('nombresFantasia')


@login_required(login_url='login')
def presentaciones(request):
    filters = get_filtros(request.GET, models.Presentacion)
    mfilters = dict(filter(lambda v: v[0] in models.Presentacion.FILTROS, filters.items()))
    presentaciones = models.Presentacion.objects.filter(**mfilters)
    estadisticas = {
        'total': models.Presentacion.objects.all().count(),
        'filtrados': presentaciones.count()
    }
    return render(request, "presentacion/presentaciones.html",{"presentaciones": presentaciones, "filtros": filters, 'estadisticas': estadisticas})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def presentacion_add(request):
    if request.method == "POST":
        form = forms.PresentacionFormAdd(request.POST)
        if form.is_valid():
            form.save()
            if '_volver' in request.POST:
                return redirect('presentaciones')
            else:
                request.session['successAdd'] = True
                return redirect('presentacion_add')
    else:
        form = forms.PresentacionFormAdd()

    successAdd = hubo_alta(request.session)
    return render(request, "presentacion/presentacionAdd.html", {'form': form, 'successAdd': successAdd})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def presentacion_update(request, id_presentacion):
    presentacion = get_object_or_404(models.Presentacion, pk=id_presentacion)
    if request.method == "POST":
        form = forms.PresentacionFormUpdate(request.POST, instance=presentacion)
        if form.is_valid():
            form.save()
            return redirect('presentaciones')
    else:
        form = forms.PresentacionFormUpdate(instance=presentacion)
    return render(request, "presentacion/presentacionUpdate.html", {'form': form, 'presentacion': presentacion})


@json_view
@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def presentacion_try_delete(request, id_presentacion):
    infoBaja = utils.puedo_eliminar_presentacion(id_presentacion)
    return infoBaja


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def presentacion_delete(request, id_presentacion):
    infoBaja = utils.puedo_eliminar_presentacion(id_presentacion)
    if infoBaja['success']:
        clinica = models.Presentacion.objects.get(pk=id_presentacion)
        clinica.delete()
        return redirect('presentaciones')


@login_required(login_url='login')
def medicamentos(request):
    filters = get_filtros(request.GET, models.Medicamento)
    mfilters = dict(filter(lambda v: v[0] in models.Medicamento.FILTROS, filters.items()))
    medicamentos = models.Medicamento.objects.filter(**mfilters)
    estadisticas = {
        'total': models.Medicamento.objects.all().count(),
        'filtrados': medicamentos.count()
    }
    return render(request, "medicamento/medicamentos.html", {"medicamentos": medicamentos, "filtros": filters, 'estadisticas': estadisticas})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def medicamento_add(request):
    if request.method == 'POST':
        medicamento_form = forms.MedicamentoForm(request.POST)
        dosis_formset = forms.DosisFormSet(request.POST)
        if medicamento_form.is_valid() and dosis_formset.is_valid():
            medicamento = medicamento_form.save()
            for dosis_form in dosis_formset:
                if dosis_form.cleaned_data:
                    dosis = dosis_form.save(commit=False)
                    dosis.medicamento = medicamento
                    dosis.save()
            if '_volver' in request.POST:
                return redirect('medicamentos')
            else:
                request.session['successAdd'] = True
                return redirect('medicamento_add')
    else:
        dosis_formset = forms.DosisFormSet()
        medicamento_form = forms.MedicamentoForm()

    successAdd = hubo_alta(request.session)

    return render(request, "medicamento/medicamentoAdd.html", {
        "medicamento_form": medicamento_form,
        "dosis_formset": dosis_formset,
        "successAdd": successAdd
    })


@permission_required('usuarios.encargado_stock', login_url='login')
@login_required(login_url='login')
def medicamento_updateStockMinimo(request, id_medicamento):
    medicamento = get_object_or_404(models.Medicamento, pk=id_medicamento)
    if request.method == "POST":
        form = forms.MedicamentoFormUpdateStockMinimo(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()
            return redirect('medicamentos')
    else:
        form = forms.MedicamentoFormUpdateStockMinimo(instance=medicamento)
    return render(request, "medicamento/medicamentoUpdateStockMinimo.html", {'form': form, 'medicamento': medicamento})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def medicamento_updatePrecioVenta(request, id_medicamento):
    medicamento = get_object_or_404(models.Medicamento, pk=id_medicamento)
    if request.method == "POST":
        form = forms.MedicamentoFormUpdatePrecioVenta(request.POST, instance=medicamento)
        if form.is_valid():
            form.save()
            return redirect('medicamentos')
    else:
        form = forms.MedicamentoFormUpdatePrecioVenta(instance=medicamento)
    return render(request, "medicamento/medicamentoUpdatePrecioVenta.html", {'form': form, 'medicamento': medicamento})


@json_view
@login_required(login_url='login')
def medicamento_verLotes(request, id_medicamento):
    lotes_json = []
    medicamento = models.Medicamento.objects.get(pk=id_medicamento)
    lotes = medicamento.get_lotes_activos()
    for lote in lotes:
        lotes_json.append(lote.to_json())

    return {'lotes': lotes_json}


@json_view
@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def medicamento_try_delete(request, id_medicamento):
    infoBaja = utils.puedo_eliminar_medicamento(id_medicamento)
    return infoBaja


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def medicamento_delete(request, id_medicamento):
    infoBaja = utils.puedo_eliminar_medicamento(id_medicamento)
    if infoBaja['success']:
        medicamento = models.Medicamento.objects.get(pk=id_medicamento)
        detallesPedidoAlaboratorio = pmodels.DetallePedidoAlaboratorio.objects.filter(medicamento=medicamento)
        pedidosAlaboratorio = set()
        for detalle in detallesPedidoAlaboratorio:
            pedidosAlaboratorio.add(detalle.pedido)

        for pedido in pedidosAlaboratorio:
            detallesDelPedido = pedido.get_detalles()
            if detallesDelPedido.count() <= 2:
                deletePedido = True
                if detallesDelPedido.count() == 2:
                    deletePedido = detallesDelPedido.filter(medicamento=medicamento).count() == 2

                if deletePedido:
                    p = pmodels.PedidoAlaboratorio.objects.get(pk=pedido.pk)
                    p.delete()

        detallesPedidoDeFarmacia = pmodels.DetallePedidoDeFarmacia.objects.filter(medicamento=medicamento)
        for detalle in detallesPedidoDeFarmacia:
            pedido = detalle.pedidoDeFarmacia
            if pedido.get_detalles().count() <= 1:
                p = pmodels.PedidoDeFarmacia.objects.get(pk=pedido.pk)
                p.delete()

        detallesPedidoDeClinica = pmodels.DetallePedidoDeClinica.objects.filter(medicamento=medicamento)
        for detalle in detallesPedidoDeClinica:
            pedido = detalle.pedidoDeClinica
            if pedido.get_detalles().count() <= 1:
                p = pmodels.PedidoDeClinica.objects.filter(pk=pedido.pk)
                p.delete()

        medicamento.delete()    
           
        return redirect('medicamentos')


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def medicamentos_topPorCantidad(request):
    form = forms.RangoFechasForm(request.GET)
    estadistica = None
    if form.is_valid():
        estadistica = utils.top_10_cantidad_medicamentos(form.clean())
        request.session['estadistica'] = estadistica
    else:
        estadistica = request.session['estadistica']
    columnChart = estadistica['columnChart']
    pieChart = estadistica['pieChart']
    return render(request, "medicamento/medicamentosTopMasSolicitadoPorCantidad.html", {'columnChart': 
            json.dumps(columnChart), 'pieChart': json.dumps(pieChart), 'form': form})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def medicamentos_topPorCantidadExcel(request):
    datos = request.session['estadistica']['excel']
    excel = io.BytesIO()
    workbook = Workbook(excel, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    titulo = workbook.add_format({
        'font_name':'Arial',
        'font_size': 12,
        'font_color': 'navy',
        'bold': True
    })
    encabezado = workbook.add_format({
        'font_name':'Arial',
        'bold': True
    })
    alignLeft = workbook.add_format({
        'align':'left',
    })
    worksheet.write('A1:B1', 'Medicamentos mas solicitados (por cantidad)', titulo)

    worksheet.set_column('B:B', 40)
    worksheet.set_column('C:C', 20)
    worksheet.write('A2', '#', encabezado)
    worksheet.write('B2', 'Medicamento', encabezado)
    worksheet.write('C2', 'Cantidad', encabezado)
    fila = 2
    tope = len(datos)
    for i in range(0, tope):
        worksheet.write(fila, 0, i + 1, alignLeft)
        worksheet.write(fila, 1, datos[i]['medicamento'], alignLeft)
        worksheet.write(fila, 2, datos[i]['cantidad'], alignLeft)
        fila += 1
    workbook.close()

    excel.seek(0)

    response = HttpResponse(excel.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=MedicamentoMasSolicitadoPorCantidad.xlsx"
    return response


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def medicamentos_topPorPedido(request):
    form = forms.RangoFechasForm(request.GET)
    estadistica = None
    if form.is_valid():
        estadistica = utils.top_10_pedido_medicamentos(form.clean())
        request.session['estadistica'] = estadistica
    else:
        estadistica = request.session['estadistica']
    columnChart = estadistica['columnChart']
    pieChart = estadistica['pieChart']
    return render(request, "medicamento/medicamentosTopMasSolicitadosPorPedido.html", {'columnChart':
            json.dumps(columnChart), 'pieChart': json.dumps(pieChart), 'form': form})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def medicamentos_topPorPedidoExcel(request):
    datos = request.session['estadistica']['excel']
    excel = io.BytesIO()
    workbook = Workbook(excel, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    titulo = workbook.add_format({
        'font_name':'Arial',
        'font_size': 12,
        'font_color': 'navy',
        'bold': True
    })
    encabezado = workbook.add_format({
        'font_name':'Arial',
        'bold': True
    })
    alignLeft = workbook.add_format({
        'align':'left',
    })
    worksheet.write('A1:B1', 'Medicamentos mas solicitados (por pedido)', titulo)

    worksheet.set_column('B:B', 40)
    worksheet.set_column('C:C', 20)
    worksheet.write('A2', '#', encabezado)
    worksheet.write('B2', 'Medicamento', encabezado)
    worksheet.write('C2', 'Cantidad', encabezado)
    fila = 2
    tope = len(datos)
    for i in range(0, tope):
        worksheet.write(fila, 0, i + 1, alignLeft)
        worksheet.write(fila, 1, datos[i]['medicamento'], alignLeft)
        worksheet.write(fila, 2, datos[i]['cantidad'], alignLeft)
        fila += 1
    workbook.close()

    excel.seek(0)

    response = HttpResponse(excel.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=MedicamentoMasSolicitadoPorPedido.xlsx"
    return response


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def medicamentos_topOrganizacionesPorCantidad(request):
    form = forms.RangoFechasMedForm(request.GET)
    estadistica = None
    if form.is_valid():
        estadistica = utils.top_10_organizaciones_cantidad_medicamentos(get_filtros_pedidos, form.clean())
        request.session['estadistica'] = estadistica
    else:
        estadistica = request.session['estadistica']
    columnChart = estadistica['columnChart']
    pieChart = estadistica['pieChart']
    return render(request, "medicamento/medicamentosTopOrganizacionesMasDemandantesCantidad.html", {'columnChart':
            json.dumps(columnChart), 'pieChart': json.dumps(pieChart), 'form': form})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def medicamentos_topOrganizacionesPorCantidadExcel(request):
    datos = request.session['estadistica']['excel']['datos']
    medicamento = request.session['estadistica']['excel']['medicamento']
    excel = io.BytesIO()
    workbook = Workbook(excel, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    titulo = workbook.add_format({
        'font_name': 'Arial',
        'font_size': 12,
        'font_color': 'navy',
        'bold': True
    })
    encabezado = workbook.add_format({
        'font_name': 'Arial',
        'bold': True
    })
    alignLeft = workbook.add_format({
        'align': 'left',
    })
    worksheet.write('A1:B1', 'Organizaciones mas demandantes del medicamento '+medicamento+' (por cantidad)', titulo)

    worksheet.set_column('B:B', 40)
    worksheet.set_column('C:C', 20)
    worksheet.write('A2', '#', encabezado)
    worksheet.write('B2', 'Organizacion', encabezado)
    worksheet.write('C2', 'Cantidad', encabezado)
    fila = 2
    tope = len(datos)
    for i in range(0, tope):
        worksheet.write(fila, 0, i + 1, alignLeft)
        worksheet.write(fila, 1, datos[i]['organizacion'], alignLeft)
        worksheet.write(fila, 2, datos[i]['cantidad'], alignLeft)
        fila += 1
    workbook.close()

    excel.seek(0)

    response = HttpResponse(excel.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=OrganizacionesMasDemandantesDeMedicamentoPorCantidad.xlsx"
    return response


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def medicamentos_topOrganizacionesPorPedidos(request):
    form = forms.RangoFechasMedForm(request.GET)
    estadistica = None
    if form.is_valid():
        estadistica = utils.top_10_organizaciones_pedidos_medicamentos(get_filtros_pedidos, form.clean())
        request.session['estadistica'] = estadistica
    else:
        estadistica = request.session['estadistica']
    columnChart = estadistica['columnChart']
    pieChart = estadistica['pieChart']
    return render(request, "medicamento/medicamentosTopOrganizacionesMasDemandantesPedidos.html", {'columnChart':
            json.dumps(columnChart), 'pieChart': json.dumps(pieChart), 'form': form})


@permission_required('usuarios.encargado_general', login_url='login')
@login_required(login_url='login')
def medicamentos_topOrganizacionesPorPedidoExcel(request):
    datos = request.session['estadistica']['excel']['datos']
    medicamento = request.session['estadistica']['excel']['medicamento']
    excel = io.BytesIO()
    workbook = Workbook(excel, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    titulo = workbook.add_format({
        'font_name':'Arial',
        'font_size': 12,
        'font_color': 'navy',
        'bold': True
    })
    encabezado = workbook.add_format({
        'font_name': 'Arial',
        'bold': True
    })
    alignLeft = workbook.add_format({
        'align': 'left',
    })
    worksheet.write('A1:B1', 'Organizaciones mas demandantes del medicamento '+medicamento+' (por pedido)', titulo)

    worksheet.set_column('B:B', 40)
    worksheet.set_column('C:C', 20)
    worksheet.write('A2', '#', encabezado)
    worksheet.write('B2', 'Organizacion', encabezado)
    worksheet.write('C2', 'Cantidad', encabezado)
    fila = 2
    tope = len(datos)
    for i in range(0, tope):
        worksheet.write(fila, 0, i + 1, alignLeft)
        worksheet.write(fila, 1, datos[i]['organizacion'], alignLeft)
        worksheet.write(fila, 2, datos[i]['cantidad'], alignLeft)
        fila += 1
    workbook.close()

    excel.seek(0)

    response = HttpResponse(excel.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = "attachment; filename=OrganizacionesMasDemandantesDeMedicamentoPorPedido.xlsx"
    return response