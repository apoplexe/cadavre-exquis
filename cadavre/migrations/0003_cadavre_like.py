# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadavre', '0002_auto_20151220_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='cadavre',
            name='like',
            field=models.IntegerField(default=0),
        ),
    ]
