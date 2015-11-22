from django.contrib import admin
from .models import RemitoMedicamentosVencido
from .models import DetalleRemitoMedicamentosVencido
from .models import PedidoDeFarmacia
from .models import DetallePedidDeFarmacia
from .models import Remito
from .models import DetalleRemito
# Register your models here.

admin.site.register(RemitoMedicamentosVencido)
admin.site.register(DetalleRemitoMedicamentosVencido)
admin.site.register(PedidoDeFarmacia)
admin.site.register(DetallePedidDeFarmacia)
admin.site.register(Remito)
admin.site.register(DetalleRemito)