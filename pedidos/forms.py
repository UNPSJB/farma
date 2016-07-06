#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from pedidos import models, utils
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import StrictButton, FormActions
from django.utils.translation import ugettext_lazy as _
from medicamentos import models as mmodels
from organizaciones import models as omodels
import datetime
import config
import re


# *******************************PEDIDO DE FARMACIA*******************************#

class PedidoDeFarmaciaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'form-pedido'
    helper.form_action = 'pedidoDeFarmacia_add'
    helper.layout = Layout(
        Field('farmacia', placeholder='Farmacia'),
        Field('fecha', placeholder='Fecha', css_class='datepicker'),
        FormActions(
            StrictButton('Crear Pedido', type="submit", css_class="btn btn-success pull-right")
        )
    )

    class Meta:
        model = models.PedidoDeFarmacia
        fields = ["farmacia", "fecha"]

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        fechaActual = datetime.date.today()
        lim = fechaActual - datetime.timedelta(weeks=config.SEMANAS_LIMITE_PEDIDO)
        if fecha:
            if fecha > fechaActual:
                raise forms.ValidationError('La fecha no puede ser mayor que la actual')
            if fecha < lim:
                raise forms.ValidationError('La fecha minima permitida es el ' + lim.strftime('%d/%m/%Y'))
        return fecha


class DetallePedidoDeFarmaciaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'form-add-detalle'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('medicamento', placeholder="Medicamento"),
        Field('cantidad', placeholder='Cantidad'),
    )

    class Meta:
        model = models.DetallePedidoDeFarmacia
        fields = ["medicamento", "cantidad"]


class UpdateDetallePedidoDeFarmaciaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'form-update-detalle'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('cantidad', placeholder='Cantidad'),
    )

    class Meta:
        model = models.DetallePedidoDeFarmacia
        fields = ["cantidad"]


# *******************************PEDIDO DE CLINICA*******************************#

class PedidoDeClinicaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'form-pedido'
    helper.form_action = 'pedidoDeClinica_add'
    helper.layout = Layout(
        Field('clinica', placeholder='Clinica'),
        Field('obraSocial', placeholder='Obra social'),
        Field('medicoAuditor', placeholder='Medico auditor'),
        Field('fecha', placeholder='Fecha', css_class='datepicker'),
        FormActions(
            StrictButton('Crear Pedido', type="submit", css_class="btn btn-success pull-right")
        )
    )

    class Meta:
        model = models.PedidoDeClinica
        fields = ["clinica", "obraSocial", "medicoAuditor", "fecha"]
        labels = {
            'obraSocial': _('Obra social'),
            'medicoAuditor': _('Medico auditor'),
        }
        widgets = {
            'obraSocial': forms.Select()
        }

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        fechaActual = datetime.date.today()
        lim = fechaActual - datetime.timedelta(weeks=config.SEMANAS_LIMITE_PEDIDO)

        if fecha:
            if fecha > fechaActual:
                raise forms.ValidationError('La fecha no puede ser mayor que la actual')

            if fecha < lim:
                raise forms.ValidationError('La fecha minima permitida es el ' + lim.strftime('%d/%m/%Y'))
        return fecha

    def clean_medicoAuditor(self):
        medico = self.cleaned_data['medicoAuditor']
        if medico and not re.match(r"^[a-zA-Z]+((\s[a-zA-Z]+)+)?$", medico):
            raise forms.ValidationError('El nombre del medico auditor solo puede contener letras y espacios')
        return medico


class DetallePedidoDeClinicaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'form-add-detalle'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        'medicamento',
        Field('cantidad', placeholder='Cantidad'),
    )

    medicamento = forms.ModelChoiceField(queryset=mmodels.Medicamento.objects.none())

    class Meta:
        model = models.DetallePedidoDeClinica
        fields = ["medicamento", "cantidad"]

    def __init__(self, *args, **kwargs):
        super(DetallePedidoDeClinicaForm, self).__init__(*args, **kwargs)
        self.fields['medicamento'].queryset = utils.get_medicamentos_con_stock()

    def is_valid(self):
        valid = super(DetallePedidoDeClinicaForm, self).is_valid()
        if not valid:
            return valid

        medicamento = self.cleaned_data.get('medicamento')
        cantidad = self.cleaned_data.get('cantidad')

        if cantidad > medicamento.get_stock():
            self.add_error('cantidad', 'No hay suficiente stock para cubrir la cantidad solicitada')
            return False
        return True


class UpdateDetallePedidoDeClinicaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'form-update-detalle'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('cantidad', placeholder='Cantidad')
    )

    class Meta:
        model = models.DetallePedidoDeClinica
        fields = ["cantidad"]

    def is_valid(self, id_medicamento):
        valid = super(UpdateDetallePedidoDeClinicaForm, self).is_valid()
        if not valid:
            return valid

        cantidad = self.cleaned_data.get('cantidad')
        medicamento = mmodels.Medicamento.objects.get(pk=id_medicamento)
        if cantidad > medicamento.get_stock():
            self.add_error('cantidad', 'No hay suficiente stock para cubrir la cantidad solicitada')
            return False
        return True


# ===================================== INICIO FORMULARIOS PEDIDOS A LABORATORIOS =====================================

def get_laboratorios_con_medicamentos():
    laboratorios_con_medicamentos = []
    laboratorios = omodels.Laboratorio.objects.all()
    for laboratorio in laboratorios:
        if mmodels.Medicamento.objects.filter(laboratorio=laboratorio).count() > 0:
            laboratorios_con_medicamentos.append(laboratorio.id)

    return omodels.Laboratorio.objects.filter(pk__in=laboratorios_con_medicamentos)


class PedidoLaboratorioForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'form-pedido'
    helper.form_action = 'pedidoAlaboratorio_add'
    helper.layout = Layout(
        Field('laboratorio'),
        FormActions(
            StrictButton('Continuar', type="submit", css_class="btn btn-success pull-right")
        )
    )

    laboratorio = forms.ModelChoiceField(queryset=omodels.Laboratorio.objects.none())

    class Meta:
        model = models.PedidoAlaboratorio
        fields = ["laboratorio"]

    def __init__(self, *args, **kwargs):
        super(PedidoLaboratorioForm, self).__init__(*args, **kwargs)
        self.fields['laboratorio'].queryset = get_laboratorios_con_medicamentos()


def DetallePedidoAlaboratorioFormFactory(laboratorio_id):
    class DetallePedidoAlaboratorioForm(forms.ModelForm):
        helper = FormHelper()
        helper.form_class = 'form-horizontal'
        helper.form_id = 'form-add-detalle'
        helper.label_class = 'col-md-3'
        helper.field_class = 'col-md-8'
        helper.layout = Layout(
            Field('medicamento', placeholder="Medicamento"),
            Field('cantidad', placeholder='Cantidad'),
        )

        medicamento = forms.ModelChoiceField(queryset=mmodels.Medicamento.objects.filter(laboratorio=laboratorio_id))

        class Meta:
            model = models.DetallePedidoAlaboratorio
            fields = ["renglon" ,  "cantidad" , "medicamento"]

        def clean_cantidad(self):
            cantidad = self.cleaned_data['cantidad']
            if not cantidad:
                raise forms.ValidationError('Debe ingresar una cantidad a pedir')
            return cantidad

    return DetallePedidoAlaboratorioForm


class UpdateDetallePedidoAlaboratorioForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'form-update-detalle'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('cantidad', placeholder='Cantidad'),
    )

    class Meta:
        model = models.DetallePedidoAlaboratorio
        fields = ["cantidad"]


# ===================================== FIN FORMULARIOS DE PEDIDOS A LABORATORIOS =====================================

def get_lotes(id_medicamento, lotesEnSesion):
    listaLotes = []
    lt = datetime.date.today() + datetime.timedelta(weeks=config.SEMANAS_LIMITE_VENCIDOS)
    lotesDb = mmodels.Lote.objects.filter(medicamento__id=id_medicamento, fechaVencimiento__gt=lt)
    for lote in lotesDb:
        listaLotes.append((lote.numero, str(lote.numero)))

    for key, value in lotesEnSesion.items():
        if value['medicamento'] == id_medicamento:
            listaLotes.append((key, str(key)))
    return listaLotes


def ControlDetallePedidoAlaboratorioFormFactory(id_medicamento, lotesEnSesion):
    class ControlDetallePedidoAlaboratorioForm(forms.Form):
        helper = FormHelper()
        helper.form_class = 'form'
        helper.form_id = 'form-add-detalle'
        helper.layout = Layout(
            Field('lote', placeholder="Lote"),
            Field('cantidad', placeholder='Cantidad recibida'),     
            FormActions(
                StrictButton('Guardar y Continuar', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                            css_class="btn btn-primary"),
                StrictButton('Guardar y Volver', type="submit", name="_volver", value="_volver", id="btn-guardar-volver", 
                            css_class="btn btn-primary"),
            )
        )
        lote = forms.ChoiceField(choices=get_lotes(id_medicamento, lotesEnSesion))
        cantidad = forms.IntegerField(label='Cantidad Recibida', min_value=1)

        def is_valid(self, cantidadPendiente):
            valid = super(ControlDetallePedidoAlaboratorioForm, self).is_valid()
            if not valid:
                return valid
    
            cantidad = self.cleaned_data.get("cantidad")
            if cantidad > cantidadPendiente:
                self.add_error('cantidad', 'La cantidad ingresada es mayor a la que este detalle indica como pendiente')
                return False
            return True

        def __init__(self, *args, **kwargs):
            super(ControlDetallePedidoAlaboratorioForm, self).__init__(*args, **kwargs)
            self.fields['lote'] = forms.ChoiceField(
                choices=get_lotes(id_medicamento, lotesEnSesion))

    return ControlDetallePedidoAlaboratorioForm


class ControlDetalleConNuevoLotePedidoAlaboratorioForm(forms.Form):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'form-add-detalle'
    helper.layout = Layout(
        Field('lote', placeholder="Lote"),
        Field('fechaVencimiento', placeholder='Fecha de Vencimiento', css_class="datepicker"),
        Field('precio', placeholder="Precio"),
        Field('cantidad', placeholder='Cantidad recibida'),     
        FormActions(
            StrictButton('Guardar y Continuar', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-primary"),
            StrictButton('Guardar y Volver', type="submit", name="_volver", value="_volver", id="btn-guardar-volver", 
                        css_class="btn btn-primary"),
        )
    )

    lote = forms.IntegerField(label='Lote', min_value=1)
    fechaVencimiento = forms.DateField(label='Fecha de vencimiento')
    precio = forms.FloatField(label='Precio', min_value=1)
    cantidad = forms.IntegerField(label='Cantidad recibida', min_value=1)

    def is_valid(self, cantidadPendiente, lotesEnSesion):
        valid = super(ControlDetalleConNuevoLotePedidoAlaboratorioForm, self).is_valid()
        if not valid:
            return valid

        lote = self.cleaned_data.get('lote') 
        cantidad = self.cleaned_data.get("cantidad")

        if lote in lotesEnSesion or mmodels.Lote.objects.filter(numero=lote).exists():
            self.add_error('lote', 'El numero de lote ya existe')
            return False

        if cantidad > cantidadPendiente:
            self.add_error('cantidad', 'La cantidad ingresada es mayor a la que este detalle indica como pendiente')
            return False

        return True

    def clean_fechaVencimiento(self):
        fechaVencimiento = self.cleaned_data['fechaVencimiento']
        fechaActual = datetime.date.today() 
        lim = fechaActual + datetime.timedelta(weeks=config.SEMANAS_LIMITE_VENCIDOS)
        if fechaVencimiento and fechaVencimiento <= lim:
            raise forms.ValidationError('No se puede ingresar lotes cuya fecha de vencimiento este dentro de los proximos 6 meses')
        return fechaVencimiento


def get_laboratorios_con_vencidos():
    labosConVencidos = []
    laboratorios = omodels.Laboratorio.objects.all()
    lt = datetime.date.today() + datetime.timedelta(weeks=config.SEMANAS_LIMITE_VENCIDOS)
    for laboratorio in laboratorios:
        count = mmodels.Lote.objects.filter(medicamento__laboratorio=laboratorio, stock__gt=0, fechaVencimiento__lte=lt).count()
        if count > 0:
            labosConVencidos.append(laboratorio.pk)

    return omodels.Laboratorio.objects.filter(pk__in=labosConVencidos)


class DevolucionMedicamentosForm(forms.ModelForm):
        helper = FormHelper()
        helper.form_class = 'form'
        helper.form_id = 'form-add-detalle'
        helper.layout = Layout(
            Field('laboratorio', placeholder="Laboratorio"),
            FormActions(
                StrictButton('Continuar', type="submit", name="_confirmar", value="_confirmar", id="btn-confirmar",
                            css_class="btn btn-success pull-right"),
            )
        )

        laboratorio = forms.ModelChoiceField(queryset=omodels.Laboratorio.objects.none())

        class Meta:
            model = models.PedidoAlaboratorio
            fields = ["laboratorio"]

        def __init__(self, *args, **kwargs):
            super(DevolucionMedicamentosForm, self).__init__(*args, **kwargs)
            self.fields['laboratorio'].queryset = get_laboratorios_con_vencidos()


class RegistrarRecepcionForm(forms.Form):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.layout = Layout(
        Field('nroRemito', placeholder="Numero de remito"),
        Field('fechaRemito', placeholder='Fecha de remito', css_class='datepicker'),
        FormActions(
            StrictButton('Continuar', type="submit", css_class="btn btn-success pull-right"),
        )
    )
    nroRemito = forms.IntegerField(label='Numero de remito', min_value=1)
    fechaRemito = forms.DateField(label='Fecha de remito')

    def clean_nroRemito(self):
        nroRemito = self.cleaned_data['nroRemito']
        if nroRemito and models.RemitoLaboratorio.objects.filter(pk=nroRemito).exists():
            raise forms.ValidationError('El número de remito ya existe')
        return nroRemito

    def clean_fechaRemito(self):
        fechaRemito = self.cleaned_data['fechaRemito']
        fechaActual = datetime.date.today()
        lim = fechaActual - datetime.timedelta(weeks=config.SEMANAS_LIMITE_PEDIDO)
        
        if fechaRemito:
            if fechaRemito > fechaActual:
                raise forms.ValidationError('La fecha no puede ser mayor que la actual')

            if fechaRemito < lim:
                raise forms.ValidationError('La fecha minima permitida es el ' + lim.strftime('%d/%m/%Y'))
        return fechaRemito

class RangoFechasForm(forms.Form):
    desde = forms.DateField(label='Fecha Desde', required=False, widget=forms.TextInput(attrs={'class':'datepicker'}))
    hasta = forms.DateField(label='Fecha Hasta', widget=forms.TextInput(attrs={'class':'datepicker'}), required=False)