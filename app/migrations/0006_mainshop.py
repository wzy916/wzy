# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-11-05 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_shop'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=251)),
                ('name', models.CharField(max_length=40)),
                ('trackid', models.CharField(max_length=30)),
                ('categoryid', models.CharField(max_length=100)),
                ('brandname', models.CharField(max_length=100)),
                ('img1', models.CharField(max_length=255)),
                ('childcid1', models.CharField(max_length=100)),
                ('productid1', models.CharField(max_length=100)),
                ('longname1', models.CharField(max_length=100)),
                ('price1', models.CharField(max_length=100)),
                ('marketprice1', models.CharField(max_length=100)),
                ('img2', models.CharField(max_length=255)),
                ('childcid2', models.CharField(max_length=100)),
                ('productid2', models.CharField(max_length=100)),
                ('longname2', models.CharField(max_length=100)),
                ('price2', models.CharField(max_length=100)),
                ('marketprice2', models.CharField(max_length=100)),
                ('img3', models.CharField(max_length=255)),
                ('childcid3', models.CharField(max_length=100)),
                ('productid3', models.CharField(max_length=100)),
                ('longname3', models.CharField(max_length=100)),
                ('price3', models.CharField(max_length=100)),
                ('marketprice3', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'axf_mainshow',
            },
        ),
    ]