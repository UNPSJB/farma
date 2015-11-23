# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '__first__'),
        ('organizaciones', '__first__'),
        ('pedidos', '0002_auto_20151119_2129'),
    ]

    operations = [
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
                ('cantidad', models.BigIntegerField()),
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
            },
        ),
        migrations.RenameModel(
            old_name='RemitoMedVencido',
            new_name='RemitoMedicamentosVencido',
        ),
        migrations.RemoveField(
            model_name='detallepedidofarmacia',
            name='medicamento',
        ),
        migrations.RemoveField(
            model_name='detallepedidofarmacia',
            name='pedidoFarmacia',
        ),
        migrations.RemoveField(
            model_name='detalleremitovencido',
            name='numeroRemito',
        ),
        migrations.RemoveField(
            model_name='pedidofarmacia',
            name='farmacia',
        ),
        migrations.AlterField(
            model_name='detalleremito',
            name='detallePedidoFarmacia',
            field=models.ForeignKey(to='pedidos.DetallePedidoDeFarmacia'),
        ),
        migrations.AlterField(
            model_name='remito',
            name='pedidoFarmacia',
            field=models.ForeignKey(to='pedidos.PedidoDeFarmacia'),
        ),
        migrations.DeleteModel(
            name='DetallePedidoFarmacia',
        ),
        migrations.DeleteModel(
            name='DetalleRemitoVencido',
        ),
        migrations.DeleteModel(
            name='PedidoFarmacia',
        ),
        migrations.AddField(
            model_name='detalleremitomedicamentosvencido',
            name='remito',
            field=models.ForeignKey(to='pedidos.RemitoMedicamentosVencido'),
        ),
        migrations.AddField(
            model_name='detallepedidodefarmacia',
            name='pedidoFarmacia',
            field=models.ForeignKey(to='pedidos.PedidoDeFarmacia'),
        ),
    ]
