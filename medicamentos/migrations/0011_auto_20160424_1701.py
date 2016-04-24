# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '0010_auto_20160424_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicamento',
            name='precioDeVenta',
            field=models.FloatField(help_text=b'Este es el precio de venta del medicamento', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(9999)]),
        ),
    ]
