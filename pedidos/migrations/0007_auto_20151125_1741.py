# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0006_auto_20151125_1505'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detallepedidodeclinica',
            old_name='pedidoClinica',
            new_name='pedidoDeClinica',
        ),
        migrations.RenameField(
            model_name='detallepedidodefarmacia',
            old_name='pedidoFarmacia',
            new_name='pedidoDeFarmacia',
        ),
    ]
