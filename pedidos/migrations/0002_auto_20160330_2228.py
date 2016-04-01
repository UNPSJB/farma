# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remitolaboratorio',
            name='id',
        ),
        migrations.AlterField(
            model_name='remitolaboratorio',
            name='nroRemito',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
    ]
