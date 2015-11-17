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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('cantidadPendiente', models.PositiveIntegerField()),
                ('estaPedido', models.BooleanField(default=False)),
                ('medicamento', models.ForeignKey(to='medicamentos.Medicamento')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Detalles de Pedidos de Farmacia',
            },
        ),
        migrations.CreateModel(
            name='DetalleRemito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.BigIntegerField()),
                ('detallePedidoFarmacia', models.ForeignKey(to='pedidos.DetallePedidoFarmacia')),
                ('lote', models.ForeignKey(to='medicamentos.Lote')),
            ],
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
                ('estado', models.CharField(max_length=25, choices=[(b'Pendiente', b'Pendiente'), (b'Parcialmente enviado', b'Parcialmente enviado'), (b'Enviado', b'Enviado')])),
                ('farmacia', models.ForeignKey(to='organizaciones.Farmacia')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Pedidos de Farmacia',
            },
        ),
        migrations.CreateModel(
            name='Remito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('pedidoFarmacia', models.ForeignKey(to='pedidos.PedidoFarmacia')),
            ],
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
            model_name='detalleremito',
            name='remito',
            field=models.ForeignKey(to='pedidos.Remito'),
        ),
        migrations.AddField(
            model_name='detallepedidofarmacia',
            name='pedidoFarmacia',
            field=models.ForeignKey(to='pedidos.PedidoFarmacia'),
        ),
    ]
