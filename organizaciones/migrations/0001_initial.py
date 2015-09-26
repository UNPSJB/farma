# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Farmacia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('razonSocial', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('mail', models.CharField(max_length=50)),
                ('localidad', models.CharField(max_length=50)),
                ('nombreEncargado', models.CharField(max_length=80)),
                ('telefono', models.CharField(max_length=80)),
                ('cuit', models.CharField(max_length=80)),
            ],
        ),
    ]
