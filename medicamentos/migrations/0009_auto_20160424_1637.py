# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '0008_auto_20160424_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicamento',
            name='precioDeVenta',
            field=models.FloatField(help_text=b'Este es el precio de venta del medicamento'),
        ),
    ]
