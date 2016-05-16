#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django import forms
from .models import Usuario
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML
from crispy_forms.bootstrap import StrictButton, FormActions, PrependedText
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UsuarioAddForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form'
    helper.form_id = 'my-form'
    helper.form_action = 'usuario_add'
    helper.layout = Layout(
        Field('username', placeholder='Nombre de Usuario'),
        Field('password', placeholder='Contraseña'),
        Field('passwordConfirmar', placeholder='Confirmar Contraseña'),
        Field('cargo', placeholder='Cargo'),
        FormActions(
            StrictButton('Registrar', type="submit", css_class="btn btn-primary"),
             HTML("<p class=\"campos-obligatorios pull-right\"><span class=\"glyphicon glyphicon-info-sign\"></span> Estos campos son obligatorios (*)</p>")
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


class UsuarioLoginForm(forms.Form):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.form_id = 'login-form'
    helper.form_action = 'login'
    helper.layout = Layout(
        PrependedText('username', '<span class="glyphicon glyphicon-user"></span>', placeholder='Nombre de Usuario'),
        PrependedText('password', '<span class="glyphicon glyphicon-lock"></span>', placeholder='Contraseña'),
        FormActions(
            StrictButton('Acceder', type="submit", css_class="btn btn-primary center-block")
        )
    )

    username = forms.CharField(label='Usuario', max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

    def __init__(self, *args, **kwargs):
        super(UsuarioLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''

    def is_valid(self):
        valid = super(UsuarioLoginForm, self).is_valid()
        if not valid:
            return valid

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            self.add_error(None, 'Usuario o contraseña incorrectos')
            return False
        else:
            if not user.is_active:
                self.add_error(None, 'Usuario inactivo')
                return False
        return True