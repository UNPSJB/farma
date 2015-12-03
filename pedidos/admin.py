from django.contrib import admin

#=========================INICIO DESDE M 1==================
from .models import RemitoMedicamentosVencido
from .models import DetalleRemitoMedicamentosVencido
from .models import PedidoDeFarmacia
from .models import DetallePedidoDeFarmacia
#from .models import RemitoPedidoDeFarmacia
#from .models import DetalleRemitoPedidoDeFarmacia
from .models import PedidoDeClinica
from .models import DetallePedidoDeClinica
from .models import RemitoPedidoDeClinica
from .models import DetalleRemitoPedidoDeClinica

#=======================FIN DESDE M 1=======================
from .models import PedidoAlaboratorio
from .models import DetallePedidoAlaboratorio

# Register your models here.
class detallePedidoLabTabularInline(admin.TabularInline):
    model = DetallePedidoAlaboratorio

class PedidoAlaboratorioAdmin(admin.ModelAdmin):
    inlines = [ detallePedidoLabTabularInline ]



admin.site.register(PedidoAlaboratorio, PedidoAlaboratorioAdmin)
admin.site.register(DetallePedidoAlaboratorio)
admin.site.register(RemitoMedicamentosVencido)
admin.site.register(DetalleRemitoMedicamentosVencido)
admin.site.register(PedidoDeFarmacia)
admin.site.register(DetallePedidoDeFarmacia)
#admin.site.register(RemitoPedidoDeFarmacia)
#admin.site.register(DetalleRemitoPedidoDeFarmacia)
#********PEDIDO Y REMITO DE CLINICA********#
admin.site.register(PedidoDeClinica)
admin.site.register(DetallePedidoDeClinica)
admin.site.register(RemitoPedidoDeClinica)
admin.site.register(DetalleRemitoPedidoDeClinica)
