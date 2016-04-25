# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentacion',
            name='descripcion',
            field=models.TextField(max_length=150),
        ),
    ]
