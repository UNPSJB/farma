# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('cargo', models.CharField(max_length=50, choices=[(b'Encargado General', b'Encargado General'), (b'Encargado Medicamentos Vencidos', b'Encargado Medicamentos Vencidos'), (b'Encargado de Stock', b'Encargado de Stock'), (b'Encargado de Pedido', b'Encargado de Pedido'), (b'Empleado de Despacho de Pedido', b'Empleado de Despacho de Pedido')])),
            ],
            options={
                'permissions': (('encargado_general', 'Cargo de encargado general'), ('encargado_medicamentos_vencidos', 'Cargo de encargado de medicamentos vencidos'), ('encargado_stock', 'Cargo Encargado de stock'), ('encargado_pedido', 'Cargo Encargado de pedido'), ('empleado_despacho_pedido', 'Cargo Encargado de despacho de pedido')),
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
