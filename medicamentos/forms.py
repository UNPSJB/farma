from django import forms
from . import models
import datetime

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
