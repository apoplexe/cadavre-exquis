# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cadavre', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sentance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sentance', models.CharField(default=b'le bourgeon dans la plaine', max_length=60)),
            ],
        ),
        migrations.RemoveField(
            model_name='cadavre',
            name='color',
        ),
        migrations.AddField(
            model_name='cadavre',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cadavre',
            name='sentance_len',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cadavre',
            name='sentance_max',
            field=models.IntegerField(default=6, validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(1000000)]),
        ),
        migrations.AddField(
            model_name='cadavre',
            name='title',
            field=models.CharField(default=b'Titre', max_length=30),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='activation_key',
            field=models.CharField(max_length=40, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default=b'avatar', upload_to=b'avatar/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(default=b'no phone', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sentance',
            name='cadavre',
            field=models.ForeignKey(to='cadavre.Cadavre'),
        ),
        migrations.AddField(
            model_name='sentance',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
