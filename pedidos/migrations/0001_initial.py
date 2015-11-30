# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '__first__'),
        ('organizaciones', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetallePedidoAlaboratorio',
            fields=[
                ('renglon', models.AutoField(serialize=False, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('cantidadPendiente', models.PositiveIntegerField()),
                ('medicamento', models.ForeignKey(to='medicamentos.Medicamento')),
            ],
        ),
        migrations.CreateModel(
            name='DetallePedidoDeFarmacia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('cantidadPendiente', models.PositiveIntegerField(default=0)),
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
                ('detallePedidoFarmacia', models.ForeignKey(to='pedidos.DetallePedidoDeFarmacia')),
                ('lote', models.ForeignKey(to='medicamentos.Lote')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleRemitoMedicamentosVencido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PedidoAlaboratorio',
            fields=[
                ('numero', models.AutoField(serialize=False, primary_key=True)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('laboratorio', models.ForeignKey(to='organizaciones.Laboratorio')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoDeFarmacia',
            fields=[
                ('nroPedido', models.AutoField(serialize=False, primary_key=True)),
                ('fecha', models.DateField()),
                ('estado', models.CharField(max_length=25, choices=[(b'Pendiente', b'Pendiente'), (b'Parcialmente enviado', b'Parcialmente enviado'), (b'Enviado', b'Enviado')])),
                ('farmacia', models.ForeignKey(to='organizaciones.Farmacia')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Pedidos de Farmacia',
                'permissions': (('generar_reporte_farmacia', 'Puede generar el reporte de pedidos a farmacia'),),
            },
        ),
        migrations.CreateModel(
            name='Remito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('pedidoFarmacia', models.ForeignKey(to='pedidos.PedidoDeFarmacia')),
            ],
        ),
        migrations.CreateModel(
            name='RemitoMedicamentosVencido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.BigIntegerField()),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='detalleremitomedicamentosvencido',
            name='remito',
            field=models.ForeignKey(to='pedidos.RemitoMedicamentosVencido'),
        ),
        migrations.AddField(
            model_name='detalleremito',
            name='remito',
            field=models.ForeignKey(to='pedidos.Remito'),
        ),
        migrations.AddField(
            model_name='detallepedidodefarmacia',
            name='pedidoFarmacia',
            field=models.ForeignKey(to='pedidos.PedidoDeFarmacia'),
        ),
        migrations.AddField(
            model_name='detallepedidoalaboratorio',
            name='pedido',
            field=models.ForeignKey(to='pedidos.PedidoAlaboratorio', null=True),
        ),
    ]
