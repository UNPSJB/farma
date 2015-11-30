# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0003_remove_detallepedidoalaboratorio_pedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallepedidoalaboratorio',
            name='pedido',
            field=models.ForeignKey(to='pedidos.PedidoAlaboratorio', null=True),
        ),
    ]
