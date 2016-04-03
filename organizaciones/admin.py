from django.contrib import admin
from .models import Farmacia, Clinica, Laboratorio
from medicamentos.models import Medicamento


class MedicamentoTabularInline(admin.TabularInline):
    model = Medicamento


class LaboratorioAdmin(admin.ModelAdmin):
    inlines = [MedicamentoTabularInline]

admin.site.register(Farmacia)
admin.site.register(Clinica)
admin.site.register(Laboratorio, LaboratorioAdmin)
