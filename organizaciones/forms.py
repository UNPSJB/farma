__author__ = 'fedde'
from django import forms
from . import models
from django.utils.translation import ugettext_lazy as _

class FarmaciaForm(forms.ModelForm):

    #razonSocial = forms.ModelChoiceField(queryset=models.Farmacia.objects.all())

    class Meta:
        model = models.Farmacia
        fields = ["razonSocial","cuit","localidad", "direccion","nombreEncargado","telefono","email"]
        labels = {
            'razonSocial': _('Razón Social'),
            'cuit': _('Cuit'),
            'localidad': _('Localidad'),
            'direccion': _('Dirección'),
            'nombreEncargado': _('Nombre del encargado'),
            'telefono': _('Teléfono'),
            'email': _('Email'),
        }

class ClinicaForm(forms.ModelForm):

    #razonSocial = forms.ModelChoiceField(queryset=models.Clinica.objects.all())
    #obraSocial = forms.ModelChoiceField(queryset=models..objects.all())

    class Meta:
        model = models.Clinica
        fields = ["razonSocial","cuit","localidad", "direccion","obraSocial","telefono","email"]
        labels = {
            'razonSocial': _('Razón Social'),
            'cuit': _('Cuit'),
            'localidad': _('Localidad'),
            'direccion': _('Dirección'),
            'obraSocial': _('Obra Social'),
            'telefono': _('Teléfono'),
            'email': _('Email'),
        }

class LaboratorioForm(forms.ModelForm):

    #razonSocial = forms.ModelChoiceField(queryset=models.Laboratorio.objects.all())

    class Meta:
        model = models.Laboratorio
        fields = ["razonSocial", "cuit","localidad","direccion","telefono","email"]
        labels = {
            'razonSocial': _('Razón Social'),
            'cuit': _('Cuit'),
            'localidad': _('Localidad'),
            'direccion': _('Dirección'),
            'telefono': _('Teléfono'),
            'email': _('Email'),
        }