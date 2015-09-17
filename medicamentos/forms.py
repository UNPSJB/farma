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