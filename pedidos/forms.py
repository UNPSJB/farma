# -*- encoding: utf-8 -*-
from django import forms
from pedidos import models, lookups
from selectable import forms as selectable
from django.core.exceptions import ObjectDoesNotExist
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
import datetime

#*******************************PEDIDO DE FARMACIA*******************************#

class PedidoDeFarmaciaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'form-pedido'
    helper.form_action = 'pedidoF_add'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('farmacia', placeholder='Farmacia'),
        Field('fecha', placeholder='Fecha', css_class='datepicker'),
    )
    class Meta:
        model = models.PedidoDeFarmacia
        fields = ["farmacia", "fecha"]
        widgets = {
            'farmacia': selectable.AutoCompleteSelectWidget(lookup_class=lookups.FarmaciaLookup),
        }

class DetallePedidoDeFarmaciaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'form-add-detalle'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        'medicamento',
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

#*******************************PEDIDO DE CLINICA*******************************#

class PedidoDeClinicaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'form-pedido'
    helper.form_action = 'pedido_de_clinica_add'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('clinica', placeholder='Clinica'),
        Field('obraSocial', placeholder='Obra Social'),
        Field('medicoAuditor', placeholder='Medico Auditor'),
        Field('fecha', placeholder='Fecha', css_class='datepicker'),
    )
    class Meta:
        model = models.PedidoDeClinica
        fields = ["clinica", "obraSocial", "medicoAuditor", "fecha"]
        widgets = {
            'clinica': selectable.AutoCompleteSelectWidget(lookup_class=lookups.ClinicaLookup),
        }

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

    class Meta:
        model = models.DetallePedidoDeClinica
        fields = ["medicamento", "cantidad"]

class UpdateDetallePedidoDeClinicaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'form-update-detalle'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('cantidad', placeholder='Cantidad'),
    )

    class Meta:
        model = models.DetallePedidoDeClinica
        fields = ["cantidad"]
