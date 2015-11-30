# -*- encoding: utf-8 -*-
from django import forms
from . import models
import datetime
from . import lookups
from selectable import forms as selectable

class RemitoForm(forms.ModelForm):

    numero = forms.ModelChoiceField(queryset=models.RemitoMedVencido.objects.all())
    day = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = models.RemitoMedVencido
        fields = ["numero", "fecha"]

class PedidoFarmaciaForm(forms.ModelForm):

    class Meta:
        model = models.PedidoFarmacia
        fields = ["farmacia", "fecha", "estado"]
        widgets = {
            'farmacia': selectable.AutoCompleteSelectWidget(lookup_class=lookups.FarmaciaLookup),
        }

    def __init__(self, *args, **kwargs):
        super(PedidoFarmaciaForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                clases = 'form-control'
                if field_name == 'fecha':
                    clases = clases + ' datepicker'
                field.widget.attrs.update({'placeholder': field.label, 'class': clases})

class DetallePedidoFarmaciaForm(forms.ModelForm):

    class Meta:
        model = models.DetallePedidoFarmacia
        fields = ["medicamento", "cantidad"]

    def __init__(self, *args, **kwargs):
        super(DetallePedidoFarmaciaForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'placeholder': field.label, 'class': 'form-control'})

class PedidoLaboratorioForm(forms.ModelForm):

    class Meta:
        model = models.PedidoAlaboratorio #models que corresponde al pedido a laboratorio
        fields = ["numero" , "fecha", "laboratorio"]

class DetallePedidoLaboratorioForm(forms.ModelForm):

    class Meta:
        model = models.DetallePedidoAlaboratorio
        fields = ["renglon" , "pedido", "cantidad" , "medicamento"]


class PedLaboratorioVerRenglonesForm(PedidoLaboratorioForm):

    def __init__(self, *args, **kwargs):
        super(PedLaboratorioVerRenglonesForm,self).__init__(*args, **kwargs)
        self.fields['numero'].widget.attrs['readonly'] = True
        self.fields['fecha'].widget.attrs['readonly'] = True
        self.fields['laboratorio'].widget.attrs['readonly'] = True