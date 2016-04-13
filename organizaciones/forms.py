# -*- encoding: utf-8 -*-
from django import forms
from organizaciones import models
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import StrictButton, FormActions
import re


class FarmaciaFormGenerico(forms.ModelForm):
    class Meta:
        model = models.Farmacia
        fields = ["razonSocial", "cuit", "localidad", "direccion", "nombreEncargado", "telefono", "email"]
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

    def clean_nombreEncargado(self):
        nombreEncargado = self.cleaned_data['nombreEncargado']
        if nombreEncargado:
            if not re.match(r"^[a-zA-Z]+((\s[a-zA-Z]+)+)?$", nombreEncargado):
                raise forms.ValidationError('El nombre del encargado solo puede contener letras y espacios')
        return nombreEncargado

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if telefono:
            if not re.match(r"^[0|4|15][0-9]+$", telefono):
                raise forms.ValidationError('telefono inválido')
        return telefono


class FarmaciaFormAdd(FarmaciaFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'my-form'
    helper.form_action = 'farmacia_add'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('razonSocial', placeholder='Razon Social'),
        Field('cuit', placeholder='Cuit',),
        Field('localidad', placeholder='Localidad'),
        Field('direccion', placeholder='Direccion'),
        Field('nombreEncargado', placeholder='Encargado'),
        Field('telefono', placeholder='Telefono'),
        Field('email', placeholder='Email'),
        FormActions(
            StrictButton('Guardar y Continuar', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-success pull-right"),
            StrictButton('Guardar y Volver', type="submit", name="_volver", value="_volver", id="btn-guardar-volver", 
                        css_class="btn btn-primary pull-right"),
        )
    )  


class FarmaciaFormUpdate(FarmaciaFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'my-form'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('razonSocial', placeholder='Razon Social', readonly=True),
        Field('cuit', placeholder='Cuit', readonly=True),
        Field('localidad', placeholder='Localidad'),
        Field('direccion', placeholder='Direccion'),
        Field('nombreEncargado', placeholder='Encargado'),
        Field('telefono', placeholder='Telefono'),
        Field('email', placeholder='Email'),
        FormActions(
            StrictButton('Guardar cambios', type="submit", id="btn-guardar", css_class="btn btn-primary pull-right"),
        )
    )  


class ClinicaFormGenerico(forms.ModelForm):
    class Meta:
        model = models.Clinica
        fields = ["razonSocial", "cuit", "localidad", "direccion", "obraSocial", "telefono", "email"]
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


class ClinicaFormAdd(ClinicaFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'my-form'
    helper.form_action = 'clinica_add'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('razonSocial', placeholder='Razon Social'),
        Field('cuit', placeholder='Cuit'),
        Field('localidad', placeholder='Localidad'),
        Field('direccion', placeholder='Direccion'),
        Field('obraSocial', placeholder='Obra Social'),
        Field('telefono', placeholder='Telefono'),
        Field('email', placeholder='Email'),
        FormActions(
            StrictButton('Guardar y Continuar', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-success pull-right"),
            StrictButton('Guardar y Volver', type="submit", name="_volver", value="_volver", id="btn-guardar-volver", 
                        css_class="btn btn-primary pull-right"),
        )
    )  


class ClinicaFormUpdate(ClinicaFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'my-form'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('razonSocial', placeholder='Razon Social', readonly=True),
        Field('cuit', placeholder='Cuit', readonly=True),
        Field('localidad', placeholder='Localidad'),
        Field('direccion', placeholder='Direccion'),
        Field('obraSocial', placeholder='Obra Social'),
        Field('telefono', placeholder='Telefono'),
        Field('email', placeholder='Email'),
        FormActions(
            StrictButton('Guardar Cambios', type="submit", id="btn-guardar-continuar", 
                        css_class="btn btn-primary pull-right"),
        )
    )  


class LaboratorioFormGenerico(forms.ModelForm):
    class Meta:
        model = models.Laboratorio
        fields = ["razonSocial", "cuit", "localidad", "direccion", "telefono", "email"]
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


class LaboratorioFormAdd(LaboratorioFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'my-form'
    helper.form_action = 'laboratorio_add'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('razonSocial', placeholder='Razon Social'),
        Field('cuit', placeholder='Cuit'),
        Field('localidad', placeholder='Localidad'),
        Field('direccion', placeholder='Direccion'),
        Field('telefono', placeholder='Telefono'),
        Field('email', placeholder='Email'),
        FormActions(
            StrictButton('Guardar y Continuar', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-success pull-right"),
            StrictButton('Guardar y Volver', type="submit", name="_volver", value="_volver", id="btn-guardar-volver", 
                        css_class="btn btn-primary pull-right"),
        )
    ) 


class LaboratorioFormUpdate(LaboratorioFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'my-form'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('razonSocial', placeholder='Razon Social', readonly=True),
        Field('cuit', placeholder='Cuit', readonly=True),
        Field('localidad', placeholder='Localidad'),
        Field('direccion', placeholder='Direccion'),
        Field('telefono', placeholder='Telefono'),
        Field('email', placeholder='Email'),
        FormActions(
            StrictButton('Guardar Cambios', type="submit", id="btn-guardar-continuar", 
                        css_class="btn btn-primary pull-right"),
        )
    )  