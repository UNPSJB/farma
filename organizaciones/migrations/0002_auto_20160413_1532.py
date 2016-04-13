# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizaciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinica',
            name='telefono',
            field=models.CharField(max_length=80, blank=True),
        ),
        migrations.AlterField(
            model_name='farmacia',
            name='telefono',
            field=models.CharField(max_length=80, blank=True),
        ),
        migrations.AlterField(
            model_name='laboratorio',
            name='telefono',
            field=models.CharField(max_length=80, blank=True),
        ),
    ]
