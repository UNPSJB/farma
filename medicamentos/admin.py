from django.contrib import admin
from .models import Monodroga
from .models import Dosis
from .models import Medicamento
from .models import Formula
from .models import Presentacion
from .models import NombreFantasia
from .models import Formula


# Register your models here.
admin.site.register(Medicamento)
admin.site.register(Monodroga)
admin.site.register(Dosis)
admin.site.register(Formula)
admin.site.register(Presentacion)
admin.site.register(NombreFantasia)