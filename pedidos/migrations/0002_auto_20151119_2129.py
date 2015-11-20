# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallepedidofarmacia',
            name='cantidadPendiente',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
