# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadavre', '0003_cadavre_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cadavre',
            name='title',
            field=models.CharField(max_length=30, default='Titre'),
        ),
        migrations.AlterField(
            model_name='sentance',
            name='sentance',
            field=models.CharField(max_length=60, default='le bourgeon dans la plaine'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(upload_to='avatar/', default='avatar'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(null=True, max_length=10, default='no phone'),
        ),
    ]
