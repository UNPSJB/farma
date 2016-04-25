# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicamentos', '0006_auto_20160424_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monodroga',
            name='nombre',
            field=models.CharField(unique=True, max_length=75, error_messages={b'unique': b' Esta monodroga ya esta cargada!'}),
        ),
    ]
