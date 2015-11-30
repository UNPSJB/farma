# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0004_detallepedidoalaboratorio_pedido'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='detallepedidofarmacia',
            options={'verbose_name_plural': 'Detalles de Pedidos de Farmacia'},
        ),
        migrations.AlterModelOptions(
            name='pedidofarmacia',
            options={'verbose_name_plural': 'Pedidos de Farmacia'},
        ),
    ]
