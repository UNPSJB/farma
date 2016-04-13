# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clinica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('razonSocial', models.CharField(max_length=50)),
                ('cuit', models.CharField(max_length=80)),
                ('localidad', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50, blank=True)),
                ('telefono', models.BigIntegerField(blank=True)),
                ('obraSocial', models.CharField(max_length=80)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Farmacia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('razonSocial', models.CharField(max_length=50)),
                ('cuit', models.CharField(max_length=80)),
                ('localidad', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50, blank=True)),
                ('telefono', models.BigIntegerField(blank=True)),
                ('nombreEncargado', models.CharField(max_length=80, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Laboratorio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('razonSocial', models.CharField(max_length=50)),
                ('cuit', models.CharField(max_length=80)),
                ('localidad', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50, blank=True)),
                ('telefono', models.BigIntegerField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
