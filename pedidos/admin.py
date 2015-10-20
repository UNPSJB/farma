from django.contrib import admin
from .models import RemitoMedVencido
from .models import DetalleRemitoVencido

# Register your models here.

admin.site.register(RemitoMedVencido)
admin.site.register(DetalleRemitoVencido)