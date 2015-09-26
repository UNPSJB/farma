__author__ = 'fedde'
from django import forms
from . import models
import datetime

class FarmaciaForm(forms.ModelForm):

    #razonSocial = forms.ModelChoiceField(queryset=models.Farmacia.objects.all())

    class Meta:
        model = models.Farmacia
        fields = ["razonSocial", "direccion","mail","localidad","nombreEncargado","telefono","cuit"]

class ClinicaForm(forms.ModelForm):

    #razonSocial = forms.ModelChoiceField(queryset=models.Clinica.objects.all())
    #obraSocial = forms.ModelChoiceField(queryset=models..objects.all())

    class Meta:
        model = models.Clinica
        fields = ["razonSocial", "direccion","mail","localidad","obraSocial","telefono","cuit"]

class LaboratorioForm(forms.ModelForm):

    #razonSocial = forms.ModelChoiceField(queryset=models.Laboratorio.objects.all())

    class Meta:
        model = models.Laboratorio
        fields = ["razonSocial", "cuit","direccion","localidad","telefono","mail"]
