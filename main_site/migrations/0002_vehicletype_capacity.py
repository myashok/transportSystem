# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-29 13:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicletype',
            name='capacity',
            field=models.IntegerField(default=4),
        ),
    ]