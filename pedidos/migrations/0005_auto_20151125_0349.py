# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0004_auto_20151123_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidodefarmacia',
            name='estado',
            field=models.CharField(max_length=25, blank=True),
        ),
    ]
