# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-06 09:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_minbtns'),
    ]

    operations = [
        migrations.AddField(
            model_name='minbtns',
            name='is_used',
            field=models.BooleanField(default=True, verbose_name='正在用'),
        ),
    ]
