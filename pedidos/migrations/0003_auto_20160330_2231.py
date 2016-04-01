# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_auto_20160330_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remitolaboratorio',
            name='nroRemito',
            field=models.BigIntegerField(unique=True, serialize=False, primary_key=True),
        ),
    ]
