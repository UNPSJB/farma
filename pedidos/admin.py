from django.contrib import admin


# =========================INICIO DESDE M 1==================

from .models import RemitoMedicamentosVencidos
from .models import DetalleRemitoMedicamentosVencido
from .models import PedidoDeFarmacia
from .models import DetallePedidoDeFarmacia
from .models import RemitoDeFarmacia
from .models import DetalleRemitoDeFarmacia
from .models import PedidoDeClinica
from .models import DetallePedidoDeClinica
from .models import RemitoDeClinica
from .models import DetalleRemitoDeClinica
from .models import RemitoLaboratorio
from .models import DetalleRemitoLaboratorio


# =======================FIN DESDE M 1=======================

from .models import PedidoAlaboratorio
from .models import DetallePedidoAlaboratorio


class detallePedidoLabTabularInline(admin.TabularInline):
    model = DetallePedidoAlaboratorio


class PedidoAlaboratorioAdmin(admin.ModelAdmin):
    inlines = [ detallePedidoLabTabularInline ]


admin.site.register(PedidoAlaboratorio, PedidoAlaboratorioAdmin)
admin.site.register(DetallePedidoAlaboratorio)
admin.site.register(RemitoMedicamentosVencidos)
admin.site.register(DetalleRemitoMedicamentosVencido)
admin.site.register(PedidoDeFarmacia)
admin.site.register(DetallePedidoDeFarmacia)
admin.site.register(RemitoDeFarmacia)
admin.site.register(DetalleRemitoDeFarmacia)

# ********PEDIDO Y REMITO DE CLINICA******** #

admin.site.register(PedidoDeClinica)
admin.site.register(DetallePedidoDeClinica)
admin.site.register(RemitoDeClinica)
admin.site.register(DetalleRemitoDeClinica)
admin.site.register(RemitoLaboratorio)
admin.site.register(DetalleRemitoLaboratorio)