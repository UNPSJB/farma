# -*- encoding: utf-8 -*-
from django import forms
from organizaciones import models
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML
from crispy_forms.bootstrap import StrictButton, FormActions, InlineField
import re


class RangoFechaReporteForm(forms.Form):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.layout = Layout(
        Field('fechaMin', placeholder='Fecha Mínima', css_class="datepicker"),
        Field('fechaMax', placeholder='Fecha Máxima', css_class="datepicker"),
        FormActions(
            StrictButton('Continuar', type="submit", css_class="btn btn-primary"),
        )
    )
    fechaMin = forms.DateField(label='Fecha Mínima')
    fechaMax = forms.DateField(label='Fecha Máxima')


class FarmaciaFormGenerico(forms.ModelForm):
    class Meta:
        model = models.Farmacia
        fields = ["razonSocial", "cuit", "localidad", "direccion", "nombreEncargado", "telefono", "email"]
        labels = {
            'razonSocial': _('Razon social'),
            'cuit': _('CUIT'),
            'localidad': _('Localidad'),
            'direccion': _('Direccion'),
            'nombreEncargado': _('Nombre de encargado'),
            'telefono': _('Telefono'),
            'email': _('Email'),
        }

    def clean_razonSocial(self):
        razonSocial = self.cleaned_data['razonSocial']
        if razonSocial:
            if not re.match(r"^[a-zA-Z\d]+((\s[a-zA-Z\d]+)+)?$", razonSocial):
                raise forms.ValidationError('La razon social no puede contener caracteres especiales')
        return razonSocial

    def clean_localidad(self):
        localidad = self.cleaned_data['localidad']
        if localidad:
            if not re.match(r"^[a-zA-Z]+((\s[a-zA-Z]+)+)?$", localidad):
                raise forms.ValidationError('La localidad solo puede contener letras y espacios')
        return localidad

    def clean_direccion(self):
        direccion = self.cleaned_data['direccion']
        if direccion:
            if not re.match(r"^[a-zA-Z\d°]+((\s[a-zA-Z\d°]+)+)?$", direccion):
                raise forms.ValidationError('La direccion no puede contener caracteres especiales, excepto "°"')
        return direccion

    def clean_nombreEncargado(self):
        nombreEncargado = self.cleaned_data['nombreEncargado']
        if nombreEncargado:
            if not re.match(r"^[a-zA-Z]+((\s[a-zA-Z]+)+)?$", nombreEncargado):
                raise forms.ValidationError('El nombre del encargado solo puede contener letras y espacios')
        return nombreEncargado


class FarmaciaFormAdd(FarmaciaFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.form_action = 'farmacia_add'
    helper.layout = Layout(
        Field('razonSocial', placeholder='Razon Social'),
        Field('cuit', placeholder='CUIT',),
        Field('localidad', placeholder='Localidad'),
        Field('direccion', placeholder='Direccion'),
        Field('nombreEncargado', placeholder='Encargado'),
        Field('telefono', placeholder='Telefono'),
        Field('email', placeholder='Email'),
        FormActions(
            StrictButton('Guardar y Continuar', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-primary"),
            StrictButton('Guardar y Volver', type="submit", name="_volver", value="_volver", id="btn-guardar-volver", 
                        css_class="btn btn-primary"),
            HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    ) 

    def clean_cuit(self):
        cuit = self.cleaned_data['cuit']
        if cuit:
            if models.Farmacia.objects.filter(cuit=cuit).exists():
                raise forms.ValidationError('Ya existe una farmacia con este CUIT')

            if models.Clinica.objects.filter(cuit=cuit).exists():
                raise forms.ValidationError('Ya existe una clínica con este CUIT')

            if models.Laboratorio.objects.filter(cuit=cuit).exists():
                raise forms.ValidationError('Ya existe un laboratorio con este CUIT')
                
            if not re.match(r"^[0-9]{2}-[0-9]{8}-[0-9]$", cuit):
                raise forms.ValidationError('CUIT inválido, por favor siga este formato xx-xxxxxxxx-x')
        return cuit 


class FarmaciaFormUpdate(FarmaciaFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.layout = Layout(
        Field('razonSocial', placeholder='Razon social', readonly=True),
        Field('cuit', placeholder='CUIT', readonly=True),
        Field('localidad', placeholder='Localidad'),
        Field('direccion', placeholder='Direccion'),
        Field('nombreEncargado', placeholder='Encargado'),
        Field('telefono', placeholder='Telefono'),
        Field('email', placeholder='Email'),
        FormActions(
            StrictButton('Guardar Cambios', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-primary"),
            HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    )  


class ClinicaFormGenerico(forms.ModelForm):
    class Meta:
        model = models.Clinica
        fields = ["razonSocial", "cuit", "localidad", "direccion", "obraSocial", "telefono", "email"]
        labels = {
            'razonSocial': _('Razon social'),
            'cuit': _('CUIT'),
            'localidad': _('Localidad'),
            'direccion': _('Direccion'),
            'obraSocial': _('Obra social'),
            'telefono': _('Telefono'),
            'email': _('Email'),
        }

    def clean_razonSocial(self):
        razonSocial = self.cleaned_data['razonSocial']
        if razonSocial:
            if not re.match(r"^[a-zA-Z\d]+((\s[a-zA-Z\d]+)+)?$", razonSocial):
                raise forms.ValidationError('La razon social no puede contener caracteres especiales')
        return razonSocial

    def clean_localidad(self):
        localidad = self.cleaned_data['localidad']
        if localidad:
            if not re.match(r"^[a-zA-Z]+((\s[a-zA-Z]+)+)?$", localidad):
                raise forms.ValidationError('La localidad solo puede contener letras y espacios')
        return localidad

    def clean_direccion(self):
        direccion = self.cleaned_data['direccion']
        if direccion:
            if not re.match(r"^[a-zA-Z\d°]+((\s[a-zA-Z\d°]+)+)?$", direccion):
                raise forms.ValidationError('La direccion no puede contener caracteres especiales, excepto "°"')
        return direccion

    def clean_obraSocial(self):
        obraSocial = self.cleaned_data['obraSocial']
        if obraSocial:
            obraSocial.upper()
            obrasSociales = obraSocial.split(',')
            for obrasSocial in obrasSociales:
                if not re.match(r"^[a-zA-Z]+((\s[a-zA-Z]+)+)?$", obrasSocial):
                    raise forms.ValidationError('Las Obras Sociales solo puede contener letras y espacios')
            return obraSocial.upper()
        return obraSocial


class ClinicaFormAdd(ClinicaFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.form_action = 'clinica_add'
    helper.layout = Layout(
        Field('razonSocial', placeholder='Razon social'),
        Field('cuit', placeholder='CUIT'),
        Field('localidad', placeholder='Localidad'),
        Field('direccion', placeholder='Direccion'),
        Field('obraSocial', placeholder='Obra social'),
        Field('telefono', placeholder='Telefono'),
        Field('email', placeholder='Email'),
        FormActions(
            StrictButton('Guardar y Continuar', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-primary"),
            StrictButton('Guardar y Volver', type="submit", name="_volver", value="_volver", id="btn-guardar-volver", 
                        css_class="btn btn-primary"),
            HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    )  

    def clean_cuit(self):
        cuit = self.cleaned_data['cuit']
        if cuit:
            if models.Farmacia.objects.filter(cuit=cuit).exists():
                raise forms.ValidationError('Ya existe una farmacia con este CUIT')

            if models.Clinica.objects.filter(cuit=cuit).exists():
                raise forms.ValidationError('Ya existe una clínica con este CUIT')

            if models.Laboratorio.objects.filter(cuit=cuit).exists():
                raise forms.ValidationError('Ya existe un laboratorio con este CUIT')

            if not re.match(r"^[0-9]{2}-[0-9]{8}-[0-9]$", cuit):
                raise forms.ValidationError('CUIT inválido, por favor siga este formato xx-xxxxxxxx-x')
        return cuit


class ClinicaFormUpdate(ClinicaFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.layout = Layout(
        Field('razonSocial', placeholder='Razon social', readonly=True),
        Field('cuit', placeholder='CUIT', readonly=True),
        Field('localidad', placeholder='Localidad'),
        Field('direccion', placeholder='Direccion'),
        Field('obraSocial', placeholder='Obra social'),
        Field('telefono', placeholder='Telefono'),
        Field('email', placeholder='Email'),
        FormActions(
            StrictButton('Guardar Cambios', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-primary"),
            HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    )  


class LaboratorioFormGenerico(forms.ModelForm):
    class Meta:
        model = models.Laboratorio
        fields = ["razonSocial", "cuit", "localidad", "direccion", "telefono", "email"]
        labels = {
            'razonSocial': _('Razon social'),
            'cuit': _('CUIT'),
            'localidad': _('Localidad'),
            'direccion': _('Direccion'),
            'telefono': _('Telefono'),
            'email': _('Email'),
        }

    def clean_razonSocial(self):
        razonSocial = self.cleaned_data['razonSocial']
        if razonSocial:
            if not re.match(r"^[a-zA-Z\d]+((\s[a-zA-Z\d]+)+)?$", razonSocial):
                raise forms.ValidationError('La razon social no puede contener caracteres especiales')
        return razonSocial

    def clean_localidad(self):
        localidad = self.cleaned_data['localidad']
        if localidad:
            if not re.match(r"^[a-zA-Z]+((\s[a-zA-Z]+)+)?$", localidad):
                raise forms.ValidationError('La localidad solo puede contener letras y espacios')
        return localidad

    def clean_direccion(self):
        direccion = self.cleaned_data['direccion']
        if direccion:
            if not re.match(r"^[a-zA-Z\d°]+((\s[a-zA-Z\d°]+)+)?$", direccion):
                raise forms.ValidationError('La direccion no puede contener caracteres especiales, excepto "°"')
        return direccion


class LaboratorioFormAdd(LaboratorioFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.form_action = 'laboratorio_add'
    helper.layout = Layout(
        Field('razonSocial', placeholder='Razon social'),
        Field('cuit', placeholder='CUIT'),
        Field('localidad', placeholder='Localidad'),
        Field('direccion', placeholder='Direccion'),
        Field('telefono', placeholder='Telefono'),
        Field('email', placeholder='Email'),
        FormActions(
            StrictButton('Guardar y Continuar', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-primary"),
            StrictButton('Guardar y Volver', type="submit", name="_volver", value="_volver", id="btn-guardar-volver", 
                        css_class="btn btn-primary"),
            HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    )

    def clean_cuit(self):
        cuit = self.cleaned_data['cuit']
        if cuit:
            if models.Farmacia.objects.filter(cuit=cuit).exists():
                raise forms.ValidationError('Ya existe una farmacia con este CUIT')

            if models.Clinica.objects.filter(cuit=cuit).exists():
                raise forms.ValidationError('Ya existe una clínica con este CUIT')

            if models.Laboratorio.objects.filter(cuit=cuit).exists():
                raise forms.ValidationError('Ya existe un laboratorio con este CUIT')

            if not re.match(r"^[0-9]{2}-[0-9]{8}-[0-9]$", cuit):
                raise forms.ValidationError('CUIT inválido, por favor siga este formato xx-xxxxxxxx-x')
        return cuit 


class LaboratorioFormUpdate(LaboratorioFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.layout = Layout(
        Field('razonSocial', placeholder='Razon social', readonly=True),
        Field('cuit', placeholder='CUIT', readonly=True),
        Field('localidad', placeholder='Localidad'),
        Field('direccion', placeholder='Direccion'),
        Field('telefono', placeholder='Telefono'),
        Field('email', placeholder='Email'),
        FormActions(
            StrictButton('Guardar Cambios', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-primary"),
            HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    )  
