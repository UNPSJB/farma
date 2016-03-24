# -*- encoding: utf-8 -*-
from django import forms
from . import models
from pedidos import models, lookups, utils
from selectable import forms as selectable
from django.core.exceptions import ObjectDoesNotExist
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from crispy_forms.bootstrap import StrictButton, FormActions
from django.utils.translation import ugettext_lazy as _
import datetime
from . import lookups
from selectable import forms as selectable
from medicamentos import models as mmodels
from organizaciones import models as omodels

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
        Field('fecha', placeholder='Fecha', css_class='datepicker')
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


def get_medicamentos_con_stock():
    medicamentos_con_stock = []
    medicamentos = mmodels.Medicamento.objects.all()
    for medicamento in medicamentos:
        lotes = mmodels.Lote.objects.filter(medicamento=medicamento)
        if lotes.count() > 0:
            hayStock = False
            for lote in lotes:
                if lote.stock > 0:
                    hayStock = True
                    break

            if hayStock:
                medicamentos_con_stock.append(medicamento.id)
    return mmodels.Medicamento.objects.filter(pk__in=medicamentos_con_stock)

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
        self.fields['medicamento'].queryset = get_medicamentos_con_stock()


    def clean_cantidad(self):
        return validarCantidad(self.cleaned_data['cantidad'])

    def is_valid(self):
        valid = super(DetallePedidoDeClinicaForm, self).is_valid()
        if not valid:
            return valid

        medicamento = self.cleaned_data.get('medicamento')
        cantidad = self.cleaned_data.get('cantidad')

        if cantidad > utils.get_stock_total(medicamento):
            self.add_error('cantidad', 'No hay suficiente stock para cubrir la cantidad indicada')
            return False
        return True

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

    def is_valid(self, id_medicamento):
        valid = super(UpdateDetallePedidoDeClinicaForm, self).is_valid()
        if not valid:
            return valid

        cantidad = self.cleaned_data.get('cantidad')
        medicamento = mmodels.Medicamento.objects.get(pk=id_medicamento)
        if cantidad > utils.get_stock_total(medicamento):
            self.add_error('cantidad', 'No hay suficiente stock para cubrir la cantidad indicada')
            return False
        return True

#========================================INICIO FORMULARIOS PEDIDOS A LABORATORIOS========================================================
def get_laboratorios_con_medicamentos():
    laboratorios_con_medicamentos = []
    laboratorios = omodels.Laboratorio.objects.all()
    for laboratorio in laboratorios:
        if mmodels.Medicamento.objects.filter(laboratorio = laboratorio).count() > 0:
            laboratorios_con_medicamentos.append(laboratorio.id)

    return omodels.Laboratorio.objects.filter(pk__in=laboratorios_con_medicamentos)

class PedidoLaboratorioForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('laboratorio'),
        FormActions(
                StrictButton('Crear Pedido', type="submit", id="btn-guardar-continuar", css_class="btn btn-success pull-right")
                )
    )

    laboratorio=forms.ModelChoiceField(queryset=omodels.Laboratorio.objects.none())

    class Meta:
        model = models.PedidoAlaboratorio #models que corresponde al pedido a laboratorio
        fields = ["laboratorio"]#campos del pedido a laboratorio (la fecha se obtiene del sistema y el numero es autogenerado)

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

def get_lotes(id_medicamento, lotesEnSesion):
    listaLotes = []
    lotesDb = mmodels.Lote.objects.filter(medicamento__id=id_medicamento)
    for lote in lotesDb:
        listaLotes.append((lote.numero, str(lote.numero)))

    for key,value in lotesEnSesion.items():
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
                            css_class="btn btn-success pull-right"),
                StrictButton('Guardar y Volver', type="submit", name="_volver", value="_volver", id="btn-guardar-volver", 
                            css_class="btn btn-primary pull-right"),
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
                        css_class="btn btn-success pull-right"),
            StrictButton('Guardar y Volver', type="submit", name="_volver", value="_volver", id="btn-guardar-volver", 
                        css_class="btn btn-primary pull-right"),
        )
    )
    lote = forms.CharField(label='Lote', max_length=30)
    fechaVencimiento = forms.DateField(label= 'Fecha de Vencimiento')
    precio = forms.FloatField(label= 'Precio', min_value=1)
    cantidad = forms.IntegerField(label='Cantidad Recibida', min_value=1)

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