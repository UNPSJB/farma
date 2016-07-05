#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.conf import settings
from django import forms
from . import models
from . import lookups
from django.forms.formsets import BaseFormSet, formset_factory
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML
from crispy_forms.bootstrap import StrictButton, FormActions
from selectable import forms as selectable
import re


class MonodrogaFormGenerico(forms.ModelForm):
    class Meta:
        model = models.Monodroga
        fields = ["nombre"]
        labels = {
            'nombre': _('Nombre')
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if nombre:
            if not re.match(r"^[a-zA-Z]+((\s[a-zA-Z]+)+)?$", nombre):
                raise forms.ValidationError('El nombre de la monodroga solo puede contener letras y espacios')
        return nombre


class MonodrogaFormAdd(MonodrogaFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.form_action = 'monodroga_add'
    helper.layout = Layout(
        Field('nombre', placeholder='Nombre'),
        FormActions(
            StrictButton('Guardar y Continuar', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-primary"),
            StrictButton('Guardar y Volver', type="submit", name="_volver", value="_volver", id="btn-guardar-volver", 
                        css_class="btn btn-primary"),
            HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    )  


class MonodrogaFormUpdate(MonodrogaFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.layout = Layout(
        Field('nombre', placeholder='Nombre'),
        FormActions(
            StrictButton('Guardar Cambios', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-primary"),
            HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    )  


class NombreFantasiaFormGenerico(forms.ModelForm):
    class Meta:
        model = models.NombreFantasia
        fields = ["nombreF"]
        labels = {
            'nombreF': _('Nombre')
        }

    def clean_nombreF(self):
        nombreF = self.cleaned_data['nombreF']
        if nombreF:
            if not re.match(r"^[a-zA-Z\d]+((\s[a-zA-Z\d]+)+)?$", nombreF):
                raise forms.ValidationError('El nombre fantasia no puede contener caracteres especiales')
        return nombreF


class NombreFantasiaFormAdd(NombreFantasiaFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.form_action = 'nombreFantasia_add'
    helper.layout = Layout(
        Field('nombreF', placeholder='Nombre'),
        FormActions(
            StrictButton('Guardar y Continuar', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-primary"),
            StrictButton('Guardar y Volver', type="submit", name="_volver", value="_volver", id="btn-guardar-volver", 
                        css_class="btn btn-primary"),
            HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    )  


class NombreFantasiaFormUpdate(NombreFantasiaFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.layout = Layout(
        Field('nombreF', placeholder='Nombre'),
        FormActions(
            StrictButton('Guardar Cambios', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-primary"),
            HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    )  


class PresentacionFormGenerico(forms.ModelForm):
    class Meta:
        model = models.Presentacion
        fields = ["descripcion", "unidadMedida", "cantidad"]
        labels = {
            'descripcion': _('Descripcion'),
            'unidadMedida': _('Unidad de Medida'),
            'cantidad': _('Cantidad')
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion']
        if descripcion:
            if not re.match(r"^[a-zA-Z]+((\s[a-zA-Z]+)+)?$", descripcion):
                raise forms.ValidationError('La descripcion no puede contener caracteres especiales o numeros')
        return descripcion

    def clean_unidadMedida(self):
        unidadMedida = self.cleaned_data['unidadMedida']
        if unidadMedida:
            if not re.match(r"^[a-zA-Z]+((\s[a-zA-Z]+)+)?$", unidadMedida):
                raise forms.ValidationError('La unidad de medida solo puede contener letras y espacios')
        return unidadMedida


class PresentacionFormAdd(PresentacionFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.form_action = 'presentacion_add'
    helper.layout = Layout(
        Field('descripcion', placeholder='Descripcion'),
        Field('unidadMedida', placeholder='Unidad de Medida'),
        Field('cantidad', placeholder='Cantidad'),
        FormActions(
            StrictButton('Guardar y Continuar', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-primary"),
            StrictButton('Guardar y Volver', type="submit", name="_volver", value="_volver", id="btn-guardar-volver", 
                        css_class="btn btn-primary"),
            HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    ) 


class PresentacionFormUpdate(PresentacionFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.layout = Layout(
        Field('descripcion', placeholder='Descripcion'),
        Field('unidadMedida', placeholder='Unidad de Medida'),
        Field('cantidad', placeholder='Cantidad'),
        FormActions(
            StrictButton('Guardar Cambios', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-primary"),
            HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    )  


class RelatedFieldWidgetCanAdd(widgets.Select):
    def __init__(self, related_model, related_url=None, *args, **kw):
        super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)
        if not related_url:
            rel_to = related_model
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = 'admin:%s_%s_add' % info
        self.related_url = related_url

    def render(self, name, value, *args, **kwargs):
        self.related_url = reverse(self.related_url)
        output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs),
                  u'<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' %
                  (self.related_url, name),
                  u'<img src="%sadmin/img/icon_addlink.gif" width="15" height="15" align="right" margin-top="10px" alt="%s"/></a>' % (
                  settings.STATIC_URL, 'Add Another')]
        return mark_safe(u''.join(output))


class MedicamentoForm(forms.ModelForm):
    nombreFantasia = forms.ModelChoiceField(
        label="Nombre fantasia",
        required=True,
        queryset=models.NombreFantasia.objects.all()
    )

    presentacion = forms.ModelChoiceField(
        required=True,
        queryset=models.Presentacion.objects.all()
    )

    laboratorio = forms.ModelChoiceField(
        required=True,
        queryset=models.Laboratorio.objects.all()
    )

    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.form_tag = False
    helper.layout = Layout(
        Field('nombreFantasia', placeholder='Nombre Fantasía'),
        Field('codigoBarras', placeholder='Código de Barras'),
        Field('stockMinimo', placeholder='Stock Mínimo'),
        Field('presentacion', placeholder='Presentacion'),
        Field('precioDeVenta', placeholder='Precio de Venta'),
        Field('laboratorio', placeholder='Laboratorio')
    )  

    class Meta:
        model = models.Medicamento
        fields = ["nombreFantasia", "codigoBarras", "stockMinimo","presentacion", "precioDeVenta", "laboratorio"]

    def clean_precioDeVenta(self):
        precioDeVenta = self.cleaned_data['precioDeVenta']
        if precioDeVenta and (precioDeVenta < 0):
                raise forms.ValidationError('El Precio de venta debe ser mayor a cero')
        return precioDeVenta

    def clean_codigoBarras(self):
        codigoBarras = self.cleaned_data['codigoBarras']
        if codigoBarras:
            if not re.match(r"^[0-9]+((\s[0-9]+)+)?$", codigoBarras):
                raise forms.ValidationError('El codigo de barras solo puede contener numeros')
        return codigoBarras


class MedicamentoFormUpdateStockMinimo(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.layout = Layout(
        Field('stockMinimo', placeholder='Stock Minimo'),
        FormActions( 
            StrictButton('Guardar Cambios', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-primary"),
            HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    ) 

    class Meta:
        model = models.Medicamento
        fields = ["stockMinimo"]
        labels = {
            'stockMinimo': _('Stock Minimo')
        }


class MedicamentoFormUpdatePrecioVenta(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.layout = Layout(
        Field('precioDeVenta', placeholder='Precio de Venta'),
        FormActions( 
            StrictButton('Guardar Cambios', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-primary"),
            HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
        )
    ) 

    class Meta:
        model = models.Medicamento
        fields = ["precioDeVenta"]
        labels = {
            'precioDeVenta': _('Precio de Venta')
        }


class DosisForm(forms.ModelForm):
    class Meta:
        model = models.Dosis
        fields = ["monodroga", "cantidad", "unidad"]
        widgets = {
            'monodroga': selectable.AutoCompleteSelectWidget(lookup_class=lookups.MonodrogaLookup),
        }

    def clean_monodroga(self):
        monodroga = self.cleaned_data['monodroga']
        if not monodroga:
            raise forms.ValidationError('Error monodroga')
        return monodroga


class DosisFormSetBase(BaseFormSet):
    def is_valid(self):
        ret = super(DosisFormSetBase, self).is_valid()
        formula = set()
        for form in self.forms:
            mono = form.cleaned_data.get("monodroga")
            if mono:
                if mono.pk in formula:
                    raise forms.ValidationError("No se puede cargar una monodroga repetida")
                formula.add(mono)
        return ret

    def clean_monodroga(self):
        monodroga = self.cleaned_data['monodroga']
        return monodroga

DosisFormSet = formset_factory(DosisForm, formset=DosisFormSetBase, min_num=1)


class RangoFechasForm(forms.Form):
    desde = forms.DateField(label='Fecha Desde', widget=forms.TextInput(attrs={'class': 'datepicker'})
                            , required=False)
    hasta = forms.DateField(label='Fecha Hasta', widget=forms.TextInput(attrs={'class': 'datepicker'})
                            , required=False)


class RangoFechasMedForm(forms.Form):
    desde = forms.DateField(label='Fecha Desde', widget=forms.TextInput(attrs={'class': 'datepicker'})
                            , required=False)
    hasta = forms.DateField(label='Fecha Hasta', widget=forms.TextInput(attrs={'class': 'datepicker'})
                            , required=False)
    medicamento = forms.ModelChoiceField(queryset=models.Medicamento.objects.all(), required=False)
