#!/usr/bin/python
# -*- encoding: utf-8 -*-

from django import forms
from .models import Usuario
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import StrictButton, FormActions
from django.contrib.auth.models import User


class UsuarioAddForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'my-form'
    helper.form_action = 'usuario_add'
    helper.label_class = 'col-md-3'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        Field('username', placeholder='Nombre de Usuario'),
        Field('password', placeholder='Contraseña'),
        Field('passwordConfirmar', placeholder='Confirmar Contraseña'),
        Field('cargo', placeholder='Cargo'),
        FormActions(
            StrictButton('Registrar', type="submit", css_class="btn btn-success pull-right")
        )
    )

    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    passwordConfirmar = forms.CharField(widget=forms.PasswordInput, label='Confirmar Contraseña')

    class Meta:
        model = Usuario
        fields = ['username', 'password', 'cargo']
        labels = {
            'username': _('Nombre de Usuario'),
            'cargo': _('Cargo')
        }

    def __init__(self, *args, **kwargs):
        super(UsuarioAddForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None

    def clean_username(self):
        username = self.cleaned_data['username']
        if username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError('El nombre de usuario no está disponible')
        return username

    def clean(self):
        cleaned_data = super(UsuarioAddForm, self).clean()
        password = cleaned_data.get("password")
        passwordConfirmar = cleaned_data.get("passwordConfirmar")

        if password != passwordConfirmar:
            self.add_error(None, "Las contraseñas no coinciden")




