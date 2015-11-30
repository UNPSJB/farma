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
            name='DetallePedidoDeClinica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('medicamento', models.ForeignKey(to='medicamentos.Medicamento')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Detalles de Pedidos de Clinica',
            },
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
            name='DetalleRemitoMedicamentosVencido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DetalleRemitoPedidoDeClinica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('detallePedidoDeClinica', models.ForeignKey(to='pedidos.DetallePedidoDeClinica')),
                ('lote', models.ForeignKey(to='medicamentos.Lote')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleRemitoPedidoDeFarmacia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('detallePedidoDeFarmacia', models.ForeignKey(to='pedidos.DetallePedidoDeFarmacia')),
                ('lote', models.ForeignKey(to='medicamentos.Lote')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoDeClinica',
            fields=[
                ('nroPedido', models.AutoField(serialize=False, primary_key=True)),
                ('fecha', models.DateField()),
                ('estado', models.CharField(max_length=25, choices=[(b'pendiente', b'Pendiente'), (b'parcialmente enviado', b'Parcialmente enviado'), (b'enviado', b'Enviado')])),
                ('obraSocial', models.CharField(max_length=80)),
                ('medicoAuditor', models.CharField(max_length=80)),
                ('clinica', models.ForeignKey(to='organizaciones.Clinica')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Pedidos de Clinica',
            },
        ),
        migrations.CreateModel(
            name='PedidoDeFarmacia',
            fields=[
                ('nroPedido', models.AutoField(serialize=False, primary_key=True)),
                ('fecha', models.DateField()),
                ('estado', models.CharField(max_length=25, blank=True)),
                ('farmacia', models.ForeignKey(to='organizaciones.Farmacia')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'Pedidos de Farmacia',
                'permissions': (('generar_reporte_farmacia', 'Puede generar el reporte de pedidos a farmacia'),),
            },
        ),
        migrations.CreateModel(
            name='RemitoMedicamentosVencido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.BigIntegerField()),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='RemitoPedidoDeClinica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('pedidoDeClinica', models.ForeignKey(to='pedidos.PedidoDeClinica')),
            ],
        ),
        migrations.CreateModel(
            name='RemitoPedidoDeFarmacia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('pedidoDeFarmacia', models.ForeignKey(to='pedidos.PedidoDeFarmacia')),
            ],
        ),
        migrations.AddField(
            model_name='detalleremitopedidodefarmacia',
            name='remito',
            field=models.ForeignKey(to='pedidos.RemitoPedidoDeFarmacia'),
        ),
        migrations.AddField(
            model_name='detalleremitopedidodeclinica',
            name='remito',
            field=models.ForeignKey(to='pedidos.RemitoPedidoDeClinica'),
        ),
        migrations.AddField(
            model_name='detalleremitomedicamentosvencido',
            name='remito',
            field=models.ForeignKey(to='pedidos.RemitoMedicamentosVencido'),
        ),
        migrations.AddField(
            model_name='detallepedidodefarmacia',
            name='pedidoDeFarmacia',
            field=models.ForeignKey(to='pedidos.PedidoDeFarmacia'),
        ),
        migrations.AddField(
            model_name='detallepedidodeclinica',
            name='pedidoDeClinica',
            field=models.ForeignKey(to='pedidos.PedidoDeClinica'),
        ),
    ]
