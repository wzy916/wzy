# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-05 16:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20181105_1044'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now=True)),
                ('update_time', models.BooleanField(default=True)),
                ('is_selected', models.BooleanField(default=True)),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Goods')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '购物车',
            },
        ),
        migrations.AlterIndexTogether(
            name='cart',
            index_together=set([('user', 'goods')]),
        ),
    ]