from django import forms
from . import models
from django.utils.translation import ugettext_lazy as _

class FarmaciaForm(forms.ModelForm):

    class Meta:
        model = models.Farmacia
        fields = ["razonSocial","cuit","localidad", "direccion","nombreEncargado","telefono","email"]
        labels = {
            'razonSocial': _('Razon Social'),
            'cuit': _('Cuit'),
            'localidad': _('Localidad'),
            'direccion': _('Direccion'),
            'nombreEncargado': _('Nombre del encargado'),
            'telefono': _('Telefono'),
            'email': _('Email'),
        }

class ClinicaForm(forms.ModelForm):

    class Meta:
        model = models.Clinica
        fields = ["razonSocial","cuit","localidad", "direccion","obraSocial","telefono","email"]
        labels = {
            'razonSocial': _('Razon Social'),
            'cuit': _('Cuit'),
            'localidad': _('Localidad'),
            'direccion': _('Direccion'),
            'obraSocial': _('Obra Social'),
            'telefono': _('Telefono'),
            'email': _('Email'),
        }

class LaboratorioForm(forms.ModelForm):

    class Meta:
        model = models.Laboratorio
        fields = ["razonSocial", "cuit","localidad","direccion","telefono","email"]
        labels = {
            'razonSocial': _('Razon Social'),
            'cuit': _('Cuit'),
            'localidad': _('Localidad'),
            'direccion': _('Direccion'),
            'telefono': _('Telefono'),
            'email': _('Email'),
        }