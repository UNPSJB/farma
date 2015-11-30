# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '__first__'),
        ('organizaciones', '__first__'),
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetallePedidoAlaboratorio',
            fields=[
                ('renglon', models.AutoField(serialize=False, primary_key=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('medicamento', models.ForeignKey(to='medicamentos.Medicamento')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoAlaboratorio',
            fields=[
                ('numero', models.PositiveIntegerField(serialize=False, primary_key=True)),
                ('fecha', models.DateField()),
                ('laboratorio', models.ForeignKey(to='organizaciones.Laboratorio')),
            ],
        ),
        migrations.AddField(
            model_name='detallepedidoalaboratorio',
            name='pedido',
            field=models.ForeignKey(to='pedidos.PedidoAlaboratorio'),
        ),
    ]
