from selectable.base import ModelLookup
from selectable.registry import registry
from organizaciones.models import Farmacia, Clinica


class FarmaciaLookup(ModelLookup):
    model = Farmacia
    search_fields = ('razonSocial__icontains', )


class ClinicaLookup(ModelLookup):
    model = Clinica
    search_fields = ('razonSocial__icontains', )

registry.register(FarmaciaLookup)
registry.register(ClinicaLookup)
