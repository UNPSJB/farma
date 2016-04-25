# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '0004_auto_20160422_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nombrefantasia',
            name='nombreF',
            field=models.CharField(unique=True, max_length=25, error_messages={b'unique': b'Este nombre de fantasia ya esta cargado!'}),
        ),
    ]
