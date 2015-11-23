# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0003_auto_20151123_1829'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pedidodefarmacia',
            options={'verbose_name_plural': 'Pedidos de Farmacia', 'permissions': (('generar_reporte_farmacia', 'Puede generar el reporte de pedidos a farmacia'),)},
        ),
    ]
