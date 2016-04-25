# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '0002_auto_20160422_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentacion',
            name='cantidad',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(9999), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='presentacion',
            name='descripcion',
            field=models.TextField(max_length=100),
        ),
    ]
