# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '0005_auto_20160424_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nombrefantasia',
            name='nombreF',
            field=models.CharField(unique=True, max_length=75, error_messages={b'unique': b'Este nombre de fantasia ya esta cargado!'}),
        ),
    ]
