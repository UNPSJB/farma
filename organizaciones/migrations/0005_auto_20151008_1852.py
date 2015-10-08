# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizaciones', '0004_auto_20151008_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmacia',
            name='mail',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
