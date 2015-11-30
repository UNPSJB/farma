# -*- encoding: utf-8 -*-
from django import forms

from pedidos import models, lookups #LINEA COMPLETA DESDE M
#from selectable import forms as selectable #LINEA COMPLETA DESDE M-->YA SE ENCUENTRA EN ESTE CODIGO
from django.core.exceptions import ObjectDoesNotExist #LINEA COMPLETA DESDE M
from crispy_forms.helper import FormHelper #LINEA COMPLETA DESDE M
from crispy_forms.layout import Layout, Field #LINEA COMPLETA DESDE M

from . import models
import datetime
from . import lookups
from selectable import forms as selectable
from medicamentos import models as mmodels

#===============================================INICIO DESDE M 2 ==========================================
class PedidoFarmaciaForm(forms.ModelForm):
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

#=============================FIN DESDE M 1==========================================================

#=============================INICIO DESDE M 2 =============================================00
#CRISPY-FORMS
class DetallePedidoFarmaciaForm(forms.ModelForm):
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

class UpdateDetallePedidoFarmaciaForm(forms.ModelForm):
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

#=============================================FIN DESDE M 2=======================================================

#========================================INICIO FORMULARIOS PEDIDOS A LABORATORIOS========================================================

class PedidoLaboratorioForm(forms.ModelForm):

    class Meta:
        model = models.PedidoAlaboratorio #models que corresponde al pedido a laboratorio
        fields = ["laboratorio"]#campos del pedido a laboratorio (la fecha se obtiene del sistema y el numero es autogenerado)



def DetallePedidoLaboratorioFormFactory(laboratorio_id):

    class DetallePedidoLaboratorioForm(forms.ModelForm):

        medicamento = forms.ModelChoiceField(queryset=mmodels.Medicamento.objects.filter(laboratorio=laboratorio_id))
        class Meta:
            model = models.DetallePedidoAlaboratorio
            fields = ["renglon" ,  "cantidad" , "medicamento"]

        def clean_cantidad(self):
            cantidad = self.cleaned_data['cantidad']
            print(cantidad)
            if not cantidad:
                raise forms.ValidationError('Debe ingresar una cantidad a pedir')
            return cantidad

    return DetallePedidoLaboratorioForm



class PedLaboratorioVerRenglonesForm(PedidoLaboratorioForm):

    def __init__(self, *args, **kwargs):
        super(PedLaboratorioVerRenglonesForm,self).__init__(*args, **kwargs)
        self.fields['numero'].widget.attrs['readonly'] = True
        self.fields['fecha'].widget.attrs['readonly'] = True
        self.fields['laboratorio'].widget.attrs['readonly'] = True

#========================================================FIN FORMULARIOS DE PEDIDOS A LABORATORIOS======================================


