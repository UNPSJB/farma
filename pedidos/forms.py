# -*- encoding: utf-8 -*-
from django import forms
from . import models
from pedidos import models, lookups
from selectable import forms as selectable
from django.core.exceptions import ObjectDoesNotExist
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import StrictButton, FormActions
from django.utils.translation import ugettext_lazy as _
import datetime
from . import lookups
from selectable import forms as selectable
from medicamentos import models as mmodels

#*******************************VALIDACION***************************************#
def validarCantidad(cantidad):
    if cantidad == 0:
            raise forms.ValidationError('La cantidad debe ser mayor a cero')
    return cantidad

#*******************************PEDIDO DE FARMACIA*******************************#

class PedidoDeFarmaciaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'form-pedido'
    helper.form_action = 'pedidoDeFarmacia_add'
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
        Field('medicamento', placeholder="Medicamento"),
        Field('cantidad', placeholder='Cantidad'),
    )

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
    helper.form_action = 'pedidoDeClinica_add'
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

#========================================INICIO FORMULARIOS PEDIDOS A LABORATORIOS========================================================

class PedidoLaboratorioForm(forms.ModelForm):

    class Meta:
        model = models.PedidoAlaboratorio #models que corresponde al pedido a laboratorio
        fields = ["laboratorio"]#campos del pedido a laboratorio (la fecha se obtiene del sistema y el numero es autogenerado)



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
            print(cantidad)
            if not cantidad:
                raise forms.ValidationError('Debe ingresar una cantidad a pedir')
            return cantidad

    return DetallePedidoAlaboratorioForm

class PedLaboratorioVerRenglonesForm(PedidoLaboratorioForm):

    def __init__(self, *args, **kwargs):
        super(PedLaboratorioVerRenglonesForm,self).__init__(*args, **kwargs)
        self.fields['numero'].widget.attrs['readonly'] = True
        self.fields['fecha'].widget.attrs['readonly'] = True
        self.fields['laboratorio'].widget.attrs['readonly'] = True

#========================================================FIN FORMULARIOS DE PEDIDOS A LABORATORIOS======================================

class ControlDetallePedidoAlaboratorioForm(forms.Form):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'form-add-detalle'
    #helper.label_class = 'col-md-3'
    #helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('lote', placeholder="Lote"),
        Field('fechaVencimiento', placeholder='Fecha de Vencimiento', css_class="datepicker"),
        Field('cantidad', placeholder='Cantidad recibida'),     
        FormActions(
            StrictButton('Guardar y Continuar', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-success pull-right"),
            StrictButton('Guardar y Volver', type="submit", name="_volver", value="_volver", id="btn-guardar-volver", 
                        css_class="btn btn-primary pull-right"),
        )
    )

    lote = forms.CharField(label='Lote', max_length=30)
    fechaVencimiento = forms.DateField(label= 'Fecha de Vencimiento')
    cantidad = forms.IntegerField(label='Cantidad Recibida', min_value=1)

    def is_valid(self, medicamento, cantidadPendiente):
        valid = super(ControlDetallePedidoAlaboratorioForm, self).is_valid()
        if not valid:
            return valid

        lote = self.cleaned_data.get('lote')      
        vencimiento = self.cleaned_data.get("fechaVencimiento")
        cantidad = self.cleaned_data.get("cantidad")
        try:
            lote_db = mmodels.Lote.objects.get(pk=lote)
            if lote_db.medicamento != medicamento:
                self.add_error('lote', 'El lote ingresado no corresponde al medicamento de este detalle')
                return False
            if lote_db.fechaVencimiento != vencimiento:
                self.add_error('fechaVencimiento', 'La fecha de vencimiento ingresada no coincide con la del lote seleccionado')
                return False

        except mmodels.Lote.DoesNotExist:
            pass

        if cantidad > cantidadPendiente:
            self.add_error('cantidad', 'La cantidad ingresada supera la cantidad pendiente de este detalle')
            return False
        return True
