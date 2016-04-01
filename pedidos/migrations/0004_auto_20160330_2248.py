# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0003_auto_20160330_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remitolaboratorio',
            name='nroRemito',
            field=models.BigIntegerField(serialize=False, primary_key=True),
        ),
    ]
