from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.conf import settings
from django import forms
from . import models
from . import lookups
from django.forms.formsets import BaseFormSet, formset_factory
from selectable import forms as selectable
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import StrictButton, FormActions
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
    helper.form_class = 'form-horizontal'
    helper.form_id = 'my-form'
    helper.form_action = 'monodroga_add'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('nombre', placeholder='Nombre'),
        FormActions(
            StrictButton('Guardar y Continuar', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-success pull-right"),
            StrictButton('Guardar y Volver', type="submit", name="_volver", value="_volver", id="btn-guardar-volver", 
                        css_class="btn btn-primary pull-right"),
        )
    )  


class MonodrogaFormUpdate(MonodrogaFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'my-form'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('nombre', placeholder='Nombre'),
        FormActions(
            StrictButton('Guardar cambios', type="submit", id="btn-guardar", css_class="btn btn-primary pull-right"),
        )
    )  


class NombreFantasiaFormGenerico(forms.ModelForm):
    class Meta:
        model = models.NombreFantasia
        fields = ["nombreF"]
        labels = {
            'nombreF': _('Nombre')
        }


class NombreFantasiaFormAdd(NombreFantasiaFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'my-form'
    helper.form_action = 'nombreFantasia_add'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('nombreF', placeholder='Nombre'),
        FormActions(
            StrictButton('Guardar y Continuar', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-success pull-right"),
            StrictButton('Guardar y Volver', type="submit", name="_volver", value="_volver", id="btn-guardar-volver", 
                        css_class="btn btn-primary pull-right"),
        )
    )  


class NombreFantasiaFormUpdate(NombreFantasiaFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'my-form'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('nombreF', placeholder='Nombre'),
        FormActions(
            StrictButton('Guardar cambios', type="submit", id="btn-guardar", css_class="btn btn-primary pull-right"),
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


class PresentacionFormAdd(PresentacionFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'my-form'
    helper.form_action = 'presentacion_add'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('descripcion', placeholder='Descripcion'),
        Field('unidadMedida', placeholder='Unidad de Medida'),
        Field('cantidad', placeholder='Cantidad'),
        FormActions(
            StrictButton('Guardar y Continuar', type="submit", name="_continuar", value="_continuar", id="btn-guardar-continuar", 
                        css_class="btn btn-success pull-right"),
            StrictButton('Guardar y Volver', type="submit", name="_volver", value="_volver", id="btn-guardar-volver", 
                        css_class="btn btn-primary pull-right"),
        )
    ) 


class PresentacionFormUpdate(PresentacionFormGenerico):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'my-form'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('descripcion', placeholder='Descripcion'),
        Field('unidadMedida', placeholder='Unidad de Medida'),
        Field('cantidad', placeholder='Cantidad'),
        FormActions(
            StrictButton('Guardar cambios', type="submit", id="btn-guardar", css_class="btn btn-primary pull-right"),
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
        output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
        output.append(u'<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
            (self.related_url, name))
        output.append(u'<img src="%sadmin/img/icon_addlink.gif" width="15" height="15" align="right" margin-top="10px" alt="%s"/></a>' % (settings.STATIC_URL, ('Add Another')))
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

    class Meta:
        model = models.Medicamento
        fields = ["nombreFantasia", "codigoBarras", "stockMinimo","presentacion", "precioDeVenta", "laboratorio"]

    def clean_precioDeVenta(self):
        precioDeVenta = self.cleaned_data['precioDeVenta']
        if (precioDeVenta) and (precioDeVenta < 0):
                raise forms.ValidationError('El Precio de venta debe ser mayor a cero')
        return precioDeVenta


class MedicamentoFormUpdateStockMinimo(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'my-form'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('stockMinimo', placeholder='Stock Minimo'),
        FormActions(
            StrictButton('Guardar cambios', type="submit", id="btn-guardar", css_class="btn btn-primary pull-right"),
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
    helper.form_class = 'form-horizontal'
    helper.form_id = 'my-form'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('precioDeVenta', placeholder='Precio de Venta'),
        FormActions(
            StrictButton('Guardar cambios', type="submit", id="btn-guardar", css_class="btn btn-primary pull-right"),
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


class DosisFormSetBase(BaseFormSet):
    def is_valid(self):
        ret = super(DosisFormSetBase, self).is_valid()
        formula = set()
        for form in self.forms:
            mono = form.cleaned_data["monodroga"].pk
            if mono in formula:
                self._non_form_errors = self.error_class(forms.ValidationError("No se puede cargar una monodroga repetida"))
                return False
            formula.add(mono)
            print(formula)
        return ret

DosisFormSet = formset_factory(DosisForm, formset=DosisFormSetBase, extra=1)
