# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizaciones', '0003_laboratorio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmacia',
            name='nombreEncargado',
            field=models.CharField(max_length=80, blank=True),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='telefono',
            field=models.CharField(max_length=80, blank=True),
        ),
    ]
