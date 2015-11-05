from django.contrib import admin
from .models import Farmacia, Clinica, Laboratorio

# Register your models here.

admin.site.register(Farmacia)
admin.site.register(Clinica)
admin.site.register(Laboratorio)
