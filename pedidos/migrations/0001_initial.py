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
            name='DetallePedidoAlaboratorio',
            fields=[
                ('renglon', models.AutoField(serialize=False, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('cantidadPendiente', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DetallePedidoDeClinica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('cantidadPendiente', models.PositiveIntegerField(default=0)),
                ('estaPedido', models.BooleanField(default=False)),
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
            name='DetalleRemitoDeClinica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('detallePedidoDeClinica', models.ForeignKey(to='pedidos.DetallePedidoDeClinica')),
                ('lote', models.ForeignKey(to='medicamentos.Lote')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleRemitoDeFarmacia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('detallePedidoDeFarmacia', models.ForeignKey(to='pedidos.DetallePedidoDeFarmacia')),
                ('lote', models.ForeignKey(to='medicamentos.Lote')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleRemitoLaboratorio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('detallePedidoLaboratorio', models.ForeignKey(to='pedidos.DetallePedidoAlaboratorio')),
                ('lote', models.ForeignKey(to='medicamentos.Lote')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleRemitoMedicamentosVencido',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('detalleRemitoLaboratorio', models.ForeignKey(to='pedidos.DetalleRemitoLaboratorio')),
                ('lote', models.ForeignKey(to='medicamentos.Lote')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoAlaboratorio',
            fields=[
                ('numero', models.AutoField(serialize=False, primary_key=True)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('estado', models.CharField(default=b'Pendiente', max_length=25, blank=True)),
                ('laboratorio', models.ForeignKey(to='organizaciones.Laboratorio')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoDeClinica',
            fields=[
                ('nroPedido', models.AutoField(serialize=False, primary_key=True)),
                ('fecha', models.DateField()),
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
            name='RemitoDeClinica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('pedidoDeClinica', models.ForeignKey(to='pedidos.PedidoDeClinica')),
            ],
        ),
        migrations.CreateModel(
            name='RemitoDeFarmacia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField()),
                ('pedidoFarmacia', models.ForeignKey(to='pedidos.PedidoDeFarmacia')),
            ],
        ),
        migrations.CreateModel(
            name='RemitoLaboratorio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nroRemito', models.BigIntegerField()),
                ('fecha', models.DateField()),
                ('laboratorio', models.ForeignKey(to='organizaciones.Laboratorio')),
                ('pedidoLaboratorio', models.ForeignKey(to='pedidos.PedidoAlaboratorio')),
            ],
        ),
        migrations.CreateModel(
            name='RemitoMedicamentosVencidos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.BigIntegerField()),
                ('fecha', models.DateField()),
                ('laboratorio', models.ForeignKey(to='organizaciones.Laboratorio')),
            ],
        ),
        migrations.AddField(
            model_name='detalleremitomedicamentosvencido',
            name='remito',
            field=models.ForeignKey(to='pedidos.RemitoMedicamentosVencidos'),
        ),
        migrations.AddField(
            model_name='detalleremitolaboratorio',
            name='remito',
            field=models.ForeignKey(to='pedidos.RemitoLaboratorio'),
        ),
        migrations.AddField(
            model_name='detalleremitodefarmacia',
            name='remito',
            field=models.ForeignKey(to='pedidos.RemitoDeFarmacia'),
        ),
        migrations.AddField(
            model_name='detalleremitodeclinica',
            name='remito',
            field=models.ForeignKey(to='pedidos.RemitoDeClinica'),
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
        migrations.AddField(
            model_name='detallepedidoalaboratorio',
            name='detallePedidoFarmacia',
            field=models.ForeignKey(blank=True, to='pedidos.DetallePedidoDeFarmacia', null=True),
        ),
        migrations.AddField(
            model_name='detallepedidoalaboratorio',
            name='medicamento',
            field=models.ForeignKey(to='medicamentos.Medicamento'),
        ),
        migrations.AddField(
            model_name='detallepedidoalaboratorio',
            name='pedido',
            field=models.ForeignKey(to='pedidos.PedidoAlaboratorio', null=True),
        ),
    ]
