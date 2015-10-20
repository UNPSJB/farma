from django import forms
from . import models
import datetime

class RemitoForm(forms.ModelForm):

    numero = forms.ModelChoiceField(queryset=models.RemitoMedVencido.objects.all())
    day = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = models.RemitoMedVencido
        fields = ["numero", "fecha"]
