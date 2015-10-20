from django import forms
from . import models
from . import lookups
import datetime
from django.forms.formsets import formset_factory
from selectable import forms as selectable
from django.utils.translation import ugettext_lazy as _

class MonodrogaForm(forms.ModelForm):
    '''
    UNIDADES = (
        (1, "Uno"),
        (2, "Dos"),
        (3, "Tres"),
    )
    unidad = forms.ModelChoiceField(queryset=models.Monodroga.objects.all())
    day = forms.DateField(initial=datetime.date.today)
   '''
    class Meta:
        model = models.Monodroga
        fields = ["nombre"]
        labels = {
            'nombre': _('Nombre')
        }

class NombreFantasiaForm(forms.ModelForm):

    #razonSocial = forms.ModelChoiceField(queryset=models.Laboratorio.objects.all())

    class Meta:
        model = models.NombreFantasia
        fields = ["nombreF"]
        labels = {
            'nombreF': _('Nombre')
        }

class PresentacionForm(forms.ModelForm):

    #razonSocial = forms.ModelChoiceField(queryset=models.Laboratorio.objects.all())

    class Meta:
        model = models.Presentacion
        fields = ["descripcion" , "unidadMedida", "cantidad"]
        labels = {
            'descripcion': _('Descripcion'),
            'unidadMedida': _('Unidad Medida'),
            'cantidad': _('Cantidad')
        }


'''

##### Forma simple dos forms para modelo
class AltaMedicamentoForm(forms.ModelForm):
    class Meta:
        model = models.Medicamento

class ModificarMedicamentoForm(forms.ModelForm):
    class Meta:
        model = models.Medicamento
        fields = ["stockMinimo","presentacion", "precio"]

###### Factroy de form medicamento
def MedicamentoFormFactory(tipo):
    class MedicamentoForm(forms.ModelForm):
        class Meta:
            model = models.Medicamento
            if tipo == 'modificar':
                fields = ["stockMinimo","presentacion", "precio"]

    return MedicamentoForm

AltaMedicamentoForm = MedicamentoFormFactory("alta")
ModificarMedicamentoForm = MedicamentoFormFactory("modificar")

'''
class MedicamentoForm(forms.ModelForm):
    class Meta:
            model = models.Medicamento
            fields = ["stockMinimo","presentacion", "precio"]


class DosisForm(forms.ModelForm):
    class Meta:
        model = models.Dosis
        fields = ["monodroga", "cantidad", "unidad"]
        widgets = {
            'monodroga': selectable.AutoCompleteSelectWidget(lookup_class=lookups.MonodrogaLookup),
        }

DosisFormSet = formset_factory(DosisForm, extra=2)