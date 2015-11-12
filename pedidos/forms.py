# -*- encoding: utf-8 -*-
from django import forms
from pedidos import models, lookups
from selectable import forms as selectable
from django.core.exceptions import ObjectDoesNotExist
import datetime

class RemitoForm(forms.ModelForm):

    numero = forms.ModelChoiceField(queryset=models.RemitoMedVencido.objects.all())
    day = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = models.RemitoMedVencido
        fields = ["numero", "fecha"]

class PedidoFarmaciaForm(forms.ModelForm):

    class Meta:
        model = models.PedidoFarmacia
        fields = ["farmacia", "fecha"]
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


class DetallePedidoFarmaciaFormUpdate(DetallePedidoFarmaciaForm):

    def __init__(self, *args, **kwargs):
        super(DetallePedidoFarmaciaFormUpdate, self).__init__(*args, **kwargs)
        self.fields['medicamento'].widget.attrs['disabled'] = True
