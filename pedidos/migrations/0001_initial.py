# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizaciones', '__first__'),
        ('medicamentos', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetallePedidoFarmacia',
            fields=[
                ('renglon', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.PositiveIntegerField()),
                ('medicamento', models.ForeignKey(to='medicamentos.Medicamento')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DetalleRemitoVencido',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('cantidad', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PedidoFarmacia',
            fields=[
                ('nroPedido', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('parcialmente enviado', 'Parcialmente enviado'), ('enviado', 'Enviado')], max_length=25)),
                ('farmacia', models.ForeignKey(to='organizaciones.Farmacia')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RemitoMedVencido',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('numero', models.BigIntegerField()),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='detalleremitovencido',
            name='numeroRemito',
            field=models.ForeignKey(to='pedidos.RemitoMedVencido'),
        ),
        migrations.AddField(
            model_name='detallepedidofarmacia',
            name='pedidoFarmacia',
            field=models.ForeignKey(to='pedidos.PedidoFarmacia'),
        ),
    ]
