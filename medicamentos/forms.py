from django import forms
from . import models
from . import lookups
import datetime
from django.forms.formsets import formset_factory
from selectable import forms as selectable

class MonodrogaForm(forms.ModelForm):
    UNIDADES = (
        (1, "Uno"),
        (2, "Dos"),
        (3, "Tres"),
    )
    unidad = forms.ModelChoiceField(queryset=models.Monodroga.objects.all())
    day = forms.DateField(initial=datetime.date.today)
    class Meta:
        model = models.Monodroga
        fields = ["unidad", "nombre"]

class NombreFantasiaForm(forms.ModelForm):

    #razonSocial = forms.ModelChoiceField(queryset=models.Laboratorio.objects.all())

    class Meta:
        model = models.NombreFantasia
        fields = ["nombreF"]

class PresentacionForm(forms.ModelForm):

    #razonSocial = forms.ModelChoiceField(queryset=models.Laboratorio.objects.all())

    class Meta:
        model = models.Presentacion
        fields = ["descripcion" , "unidadMedida", "cantidad"]

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = models.Medicamento
        fields = ["nombreFantasia", "codigoBarras", "stockMinimo","presentacion", "precio"]

class DosisForm(forms.ModelForm):
    class Meta:
        model = models.Dosis
        fields = ["monodroga", "cantidad", "unidad"]
        widgets = {
            'monodroga': selectable.AutoCompleteSelectWidget(lookup_class=lookups.MonodrogaLookup),
        }

DosisFormSet = formset_factory(DosisForm, extra=1,can_order=True,can_delete=True,max_num=1,validate_max=True,min_num=1,validate_min=True)