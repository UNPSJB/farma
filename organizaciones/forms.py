__author__ = 'fedde'
from django import forms
from . import models
import datetime

class FarmaciaForm(forms.ModelForm):

    razonSocial = forms.ModelChoiceField(queryset=models.Farmacia.objects.all())

    #day = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = models.Farmacia
        fields = ["razonSocial", "direccion","mail","localidad","nombreEncargado","telefono","cuit"]

