from django.contrib import admin
from .models import RemitoMedVencido
from .models import DetalleRemitoVencido
from .models import PedidoFarmacia
from .models import DetallePedidoFarmacia
from .models import Remito
from .models import DetalleRemito
# Register your models here.

admin.site.register(RemitoMedVencido)
admin.site.register(DetalleRemitoVencido)
admin.site.register(PedidoFarmacia)
admin.site.register(DetallePedidoFarmacia)
admin.site.register(Remito)
admin.site.register(DetalleRemito)