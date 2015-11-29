from django.contrib import admin
from .models import RemitoMedicamentosVencido
from .models import DetalleRemitoMedicamentosVencido
from .models import PedidoDeFarmacia
from .models import DetallePedidoDeFarmacia
from .models import RemitoPedidoDeFarmacia
from .models import DetalleRemitoPedidoDeFarmacia
from .models import PedidoDeClinica
from .models import DetallePedidoDeClinica
from .models import RemitoPedidoDeClinica
from .models import DetalleRemitoPedidoDeClinica
# Register your models here.

admin.site.register(RemitoMedicamentosVencido)
admin.site.register(DetalleRemitoMedicamentosVencido)
admin.site.register(PedidoDeFarmacia)
admin.site.register(DetallePedidoDeFarmacia)
admin.site.register(RemitoPedidoDeFarmacia)
admin.site.register(DetalleRemitoPedidoDeFarmacia)
#********PEDIDO Y REMITO DE CLINICA********#
admin.site.register(PedidoDeClinica)
admin.site.register(DetallePedidoDeClinica)
admin.site.register(RemitoPedidoDeClinica)
admin.site.register(DetalleRemitoPedidoDeClinica)
