from selectable.base import ModelLookup
from selectable.registry import registry
from .models import Monodroga


class MonodrogaLookup(ModelLookup):
    model = Monodroga
    search_fields = ('nombre__icontains', )

registry.register(MonodrogaLookup)