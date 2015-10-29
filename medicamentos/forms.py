from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.conf import settings


from django import forms
from . import models
from . import lookups
import datetime
from django.forms.formsets import formset_factory
from selectable import forms as selectable
from django.utils.translation import ugettext_lazy as _

class MonodrogaForm(forms.ModelForm):
    '''
    UNIDADES = (
        (1, "Uno"),
        (2, "Dos"),
        (3, "Tres"),
    )
    unidad = forms.ModelChoiceField(queryset=models.Monodroga.objects.all())
    day = forms.DateField(initial=datetime.date.today)
   '''
    class Meta:
        model = models.Monodroga
        fields = ["nombre"]
        labels = {
            'nombre': _('Nombre')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update(
            {'placeholder': 'Nombre monodroga', 'class': 'form-control'})

     

class NombreFantasiaForm(forms.ModelForm):

    #razonSocial = forms.ModelChoiceField(queryset=models.Laboratorio.objects.all())

    class Meta:
        model = models.NombreFantasia
        fields = ["nombreF"]
        labels = {
            'nombreF': _('Nombre')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombreF'].widget.attrs.update(
            {'placeholder': 'Nombre fantasía', 'class':'form-control'})

class PresentacionForm(forms.ModelForm):

    #razonSocial = forms.ModelChoiceField(queryset=models.Laboratorio.objects.all())

    class Meta:
        model = models.Presentacion
        fields = ["descripcion" , "unidadMedida", "cantidad"]
        labels = {
            'descripcion': _('Descripción'),
            'unidadMedida': _('Unidad Medida'),
            'cantidad': _('Cantidad')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs.update({
                    'placeholder': field.label,
                    'class': 'form-control'
                })


class RelatedFieldWidgetCanAdd(widgets.Select):

    def __init__(self, related_model, related_url=None, *args, **kw):

        super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

        if not related_url:
            rel_to = related_model
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = 'admin:%s_%s_add' % info

        # Be careful that here "reverse" is not allowed
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
       label = "Nombre Fantasia",
       required=True,
       queryset=models.NombreFantasia.objects.all(),
       widget=RelatedFieldWidgetCanAdd(models.NombreFantasia, related_url="nombresFantasia_add")

    )

    presentacion = forms.ModelChoiceField(
       required=True,
       queryset=models.Presentacion.objects.all(),
       widget=RelatedFieldWidgetCanAdd(models.Presentacion, related_url="presentacion")

    )

    class Meta:
        model = models.Medicamento
        fields = ["nombreFantasia", "codigoBarras", "stockMinimo","presentacion", "precio"]


class DosisForm(forms.ModelForm):
    class Meta:
        model = models.Dosis
        fields = ["monodroga", "cantidad", "unidad"]
        widgets = {
            'monodroga': selectable.AutoCompleteSelectWidget(lookup_class=lookups.MonodrogaLookup),
        }

DosisFormSet = formset_factory(DosisForm, extra=1,can_order=True,can_delete=True,max_num=1,validate_max=True,min_num=1,validate_min=True)