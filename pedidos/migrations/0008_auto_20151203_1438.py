# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0007_auto_20151125_1741'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detalleremito',
            old_name='detallePedidoFarmacia',
            new_name='detallePedidoDeFarmacia',
        ),
    ]
