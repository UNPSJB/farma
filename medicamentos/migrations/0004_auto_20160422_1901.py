# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '0003_auto_20160422_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentacion',
            name='descripcion',
            field=models.TextField(max_length=95),
        ),
        migrations.AlterField(
            model_name='presentacion',
            name='unidadMedida',
            field=models.CharField(max_length=45),
        ),
    ]
