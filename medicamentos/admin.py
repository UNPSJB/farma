from django.contrib import admin
from .models import Monodroga
from .models import Dosis
from .models import Medicamento
from .models import Presentacion
from .models import NombreFantasia
from .models import Formula
from .models import Lote
from django.contrib.auth import models as auth_models


class DosisTabularInline(admin.TabularInline):
    model = Dosis


class MedicamentoAdmin(admin.ModelAdmin):
    inlines = [DosisTabularInline]

admin.site.register(Medicamento, MedicamentoAdmin)
admin.site.register(Monodroga)
admin.site.register(Dosis)
admin.site.register(Formula)
admin.site.register(Presentacion)
admin.site.register(NombreFantasia)
admin.site.register(Lote)
admin.site.register(auth_models.Permission)