# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '__first__'),
        ('organizaciones', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetallePedidoFarmacia',
            fields=[
                ('renglon', models.AutoField(serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PedidoFarmacia',
            fields=[
                ('nroPedido', models.AutoField(serialize=False, primary_key=True)),
                ('fecha', models.DateField()),
                ('estado', models.CharField(max_length=25, choices=[(b'pendiente', b'Pendiente'), (b'parcialmente enviado', b'Parcialmente enviado'), (b'enviado', b'Enviado')])),
                ('farmacia', models.ForeignKey(to='organizaciones.Farmacia')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RemitoMedVencido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
