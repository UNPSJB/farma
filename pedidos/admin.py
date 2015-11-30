from django.contrib import admin
from .models import RemitoMedVencido
from .models import DetalleRemitoVencido
from .models import PedidoFarmacia
from .models import DetallePedidoFarmacia
from .models import PedidoAlaboratorio
from .models import DetallePedidoAlaboratorio

# Register your models here.
class detallePedidoLabTabularInline(admin.TabularInline):
    model = DetallePedidoAlaboratorio

class PedidoAlaboratorioAdmin(admin.ModelAdmin):
    inlines = [ detallePedidoLabTabularInline ]


admin.site.register(RemitoMedVencido)
admin.site.register(DetalleRemitoVencido)
admin.site.register(PedidoFarmacia)
admin.site.register(DetallePedidoFarmacia)
admin.site.register(PedidoAlaboratorio, PedidoAlaboratorioAdmin)
admin.site.register(DetallePedidoAlaboratorio)
