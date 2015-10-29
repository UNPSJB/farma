from django import forms
from organizaciones import models
from django.utils.translation import ugettext_lazy as _
import re

class FarmaciaForm(forms.ModelForm):

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'placeholder': field.label, 'class': 'form-control'})

    def clean_cuit(self):
        cuit = self.cleaned_data['cuit']
        if cuit:
            if not re.match(r"^[0-9]{2}-[0-9]{8}-[0-9]{1}$", cuit):
                raise forms.ValidationError(_('Cuit inválido, por favor siga este formato xx-xxxxxxxx-x'))
        return cuit

class ClinicaForm(forms.ModelForm):

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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'placeholder': field.label, 'class': 'form-control'})

    def clean_cuit(self):
        cuit = self.cleaned_data['cuit']
        if cuit:
            if not re.match(r"^[0-9]{2}-[0-9]{8}-[0-9]{1}$", cuit):
                raise forms.ValidationError(_('Cuit inválido, por favor siga este formato xx-xxxxxxxx-x'))
        return cuit

class LaboratorioForm(forms.ModelForm):

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'placeholder': field.label, 'class': 'form-control'})

    def clean_cuit(self):
        cuit = self.cleaned_data['cuit']
        if cuit:
            if not re.match(r"^[0-9]{2}-[0-9]{8}-[0-9]{1}$", cuit):
                raise forms.ValidationError(_('Cuit inválido, por favor siga este formato xx-xxxxxxxx-x'))
        return cuit