# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 17:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0010_auto_20171030_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trip',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bill',
            name='trip',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_site.Trip'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_site.TransportRequest'),
        ),
    ]
