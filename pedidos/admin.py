from django.contrib import admin

#=========================INICIO DESDE M 1==================
from .models import RemitoMedicamentosVencido
from .models import DetalleRemitoMedicamentosVencido
from .models import PedidoDeFarmacia
from .models import DetallePedidoDeFarmacia
from .models import Remito
from .models import DetalleRemito
#=======================FIN DESDE M 1=======================
from .models import PedidoAlaboratorio
from .models import DetallePedidoAlaboratorio

# Register your models here.
class detallePedidoLabTabularInline(admin.TabularInline):
    model = DetallePedidoAlaboratorio

class PedidoAlaboratorioAdmin(admin.ModelAdmin):
    inlines = [ detallePedidoLabTabularInline ]

#=====================INICIO DESDE M========================
admin.site.register(RemitoMedicamentosVencido)
admin.site.register(DetalleRemitoMedicamentosVencido)
admin.site.register(PedidoDeFarmacia)
admin.site.register(DetallePedidoDeFarmacia)
admin.site.register(Remito)
admin.site.register(DetalleRemito)
#===========================================================


admin.site.register(PedidoAlaboratorio, PedidoAlaboratorioAdmin)
admin.site.register(DetallePedidoAlaboratorio)
