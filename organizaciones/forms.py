# -*- encoding: utf-8 -*-
from django import forms
from organizaciones import models
from django.utils.translation import ugettext_lazy as _
import re


class FarmaciaFormGenerico(forms.ModelForm):

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


    def clean_cuit(self):
        cuit = self.cleaned_data['cuit']
        if cuit:
            if not re.match(r"^[0-9]{2}-[0-9]{8}-[0-9]{1}$", cuit):
                raise forms.ValidationError('Cuit inválido, por favor siga este formato xx-xxxxxxxx-x')
        return cuit



class FarmaciaForm(FarmaciaFormGenerico):

    def __init__(self, *args, **kwargs):
        super(FarmaciaForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'placeholder': field.label, 'class': 'form-control'})




class FarmaciaFormUpdate(FarmaciaForm):

    def __init__(self, *args, **kwargs):
        super(FarmaciaFormUpdate,self).__init__(*args, **kwargs)
        self.fields['razonSocial'].widget.attrs['readonly'] = True
        self.fields['cuit'].widget.attrs['readonly'] = True



class ClinicaFormGenerico(forms.ModelForm):

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
    
    def clean_cuit(self):
        cuit = self.cleaned_data['cuit']
        if cuit:
            if not re.match(r"^[0-9]{2}-[0-9]{8}-[0-9]{1}$", cuit):
                raise forms.ValidationError('Cuit inválido, por favor siga este formato xx-xxxxxxxx-x')
        return cuit

class ClinicaForm(ClinicaFormGenerico):

    def __init__(self, *args, **kwargs):
        super(ClinicaForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'placeholder': field.label, 'class': 'form-control'})

class ClinicaFormUpdate(ClinicaForm):

    def __init__(self, *args, **kwargs):
        super(ClinicaFormUpdate,self).__init__(*args, **kwargs)
        self.fields['razonSocial'].widget.attrs['readonly'] = True
        self.fields['cuit'].widget.attrs['readonly'] = True
    

class LaboratorioFormGenerico(forms.ModelForm):

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

    def clean_cuit(self):
        cuit = self.cleaned_data['cuit']
        if cuit:
            if not re.match(r"^[0-9]{2}-[0-9]{8}-[0-9]{1}$", cuit):
                raise forms.ValidationError('Cuit inválido, por favor siga este formato xx-xxxxxxxx-x')
        return cuit

class LaboratorioForm(LaboratorioFormGenerico):

    def __init__(self, *args, **kwargs):
        super(LaboratorioForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({'placeholder': field.label, 'class': 'form-control'})

class LaboratorioFormUpdate(LaboratorioForm):

    def __init__(self, *args, **kwargs):
        super(LaboratorioFormUpdate,self).__init__(*args, **kwargs)
        self.fields['razonSocial'].widget.attrs['readonly'] = True
        self.fields['cuit'].widget.attrs['readonly'] = True
