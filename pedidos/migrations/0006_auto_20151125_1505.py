# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '__first__'),
        ('organizaciones', '__first__'),
        ('pedidos', '0005_auto_20151125_0349'),
    ]

    operations = [
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
        migrations.AlterField(
            model_name='detalleremito',
            name='cantidad',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='detalleremitomedicamentosvencido',
            name='cantidad',
            field=models.PositiveIntegerField(),
        ),
        migrations.AddField(
            model_name='detallepedidodeclinica',
            name='pedidoClinica',
            field=models.ForeignKey(to='pedidos.PedidoDeClinica'),
        ),
    ]
