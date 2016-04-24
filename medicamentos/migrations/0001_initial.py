# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizaciones', '0002_auto_20160413_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dosis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unidad', models.PositiveIntegerField(choices=[(1, b'ml'), (2, b'mg')])),
                ('cantidad', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Formula',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dosis', models.ForeignKey(to='medicamentos.Dosis')),
            ],
        ),
        migrations.CreateModel(
            name='Lote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.PositiveIntegerField(unique=True, error_messages={b'unique': b'Este numero de lote ya esta cargado!'})),
                ('fechaVencimiento', models.DateField()),
                ('stock', models.PositiveIntegerField()),
                ('precio', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Medicamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigoBarras', models.CharField(help_text=b'Este es un valor numerico, el cual deberia ser la clave', unique=True, max_length=15, verbose_name=b'Codigo de barras', error_messages={b'unique': b' Este codigo de barras ya esta cargado!'})),
                ('stockMinimo', models.PositiveIntegerField(help_text=b'Este es el stock minimo en el cual el sistema alertara de que es necesario realizar un pedido', verbose_name=b'Stock minimo de reposicion')),
                ('precioDeVenta', models.FloatField(help_text=b'Este es el precio de venta del medicamento')),
            ],
        ),
        migrations.CreateModel(
            name='Monodroga',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=100, error_messages={b'unique': b' Esta monodroga ya esta cargada!'})),
            ],
        ),
        migrations.CreateModel(
            name='NombreFantasia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreF', models.CharField(unique=True, max_length=100, error_messages={b'unique': b'Este nombre de fantasia ya esta cargado!'})),
            ],
        ),
        migrations.CreateModel(
            name='Presentacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.TextField(max_length=100)),
                ('cantidad', models.PositiveIntegerField()),
                ('unidadMedida', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='medicamento',
            name='formulas',
            field=models.ManyToManyField(to='medicamentos.Monodroga', through='medicamentos.Dosis'),
        ),
        migrations.AddField(
            model_name='medicamento',
            name='laboratorio',
            field=models.ForeignKey(related_name='medicamentos', to='organizaciones.Laboratorio'),
        ),
        migrations.AddField(
            model_name='medicamento',
            name='nombreFantasia',
            field=models.ForeignKey(help_text=b'Este es el Nombre Comercial del medicamento', to='medicamentos.NombreFantasia'),
        ),
        migrations.AddField(
            model_name='medicamento',
            name='presentacion',
            field=models.ForeignKey(help_text=b'Esta es la forma en la que se encuentra comercialmente el Medicamento', to='medicamentos.Presentacion'),
        ),
        migrations.AddField(
            model_name='lote',
            name='medicamento',
            field=models.ForeignKey(to='medicamentos.Medicamento'),
        ),
        migrations.AddField(
            model_name='formula',
            name='monodroga',
            field=models.ForeignKey(to='medicamentos.Monodroga'),
        ),
        migrations.AddField(
            model_name='dosis',
            name='medicamento',
            field=models.ForeignKey(to='medicamentos.Medicamento'),
        ),
        migrations.AddField(
            model_name='dosis',
            name='monodroga',
            field=models.ForeignKey(to='medicamentos.Monodroga'),
        ),
    ]
