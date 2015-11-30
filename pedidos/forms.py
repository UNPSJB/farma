# -*- encoding: utf-8 -*-
from django import forms
from pedidos import models, lookups
from selectable import forms as selectable
from django.core.exceptions import ObjectDoesNotExist
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.utils.translation import ugettext_lazy as _
import datetime
from . import lookups
from selectable import forms as selectable

class RemitoForm(forms.ModelForm):
#*******************************VALIDACION***************************************#
def validarCantidad(cantidad):
    if cantidad == 0:
            raise forms.ValidationError('La cantidad debe ser mayor a cero')
    return cantidad

#*******************************PEDIDO DE FARMACIA*******************************#
    numero = forms.ModelChoiceField(queryset=models.RemitoMedVencido.objects.all())
    day = forms.DateField(initial=datetime.date.today)

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
        model = models.RemitoMedVencido
        fields = ["numero", "fecha"]

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
class PedidoFarmaciaForm(forms.ModelForm):

    class Meta:
        model = models.DetallePedidoDeFarmacia
        fields = ["medicamento", "cantidad"]

    def clean_cantidad(self):
        return validarCantidad(self.cleaned_data['cantidad'])

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

    def clean_cantidad(self):
        return validarCantidad(self.cleaned_data['cantidad'])

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
        labels = {
            'obraSocial': _('Obra Social'),
            'medicoAuditor': _('Medico Auditor'),
        }
        model = models.PedidoFarmacia
        fields = ["farmacia", "fecha", "estado"]
        widgets = {
            'clinica': selectable.AutoCompleteSelectWidget(lookup_class=lookups.ClinicaLookup),
        }

    def __init__(self, *args, **kwargs):
        super(PedidoFarmaciaForm, self).__init__(*args, **kwargs)

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

    def clean_cantidad(self):
        return validarCantidad(self.cleaned_data['cantidad'])

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

    def clean_cantidad(self):
        return validarCantidad(self.cleaned_data['cantidad'])
