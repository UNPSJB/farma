from django.contrib import admin
from .models import Monodroga
from .models import Dosis
from .models import NombreFantasia
from .models import Presentacion

# Register your models here.

admin.site.register(Monodroga)
admin.site.register(Dosis)
admin.site.register(NombreFantasia)
admin.site.register(Presentacion)