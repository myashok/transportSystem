# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-19 05:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import main_site.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0003_auto_20171115_2236'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterModelOptions(
            name='request',
            options={'ordering': ['-start_date', '-start_time']},
        ),
        migrations.AddField(
            model_name='schedule',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='driver',
            name='picture',
            field=models.ImageField(default='default.png', help_text='If not provided, default will be used', upload_to=main_site.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='request',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='request',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='picture',
            field=models.ImageField(default='school-bus.png', help_text='If not provided, default will be taken', upload_to=main_site.models.get_upload_path),
        ),
    ]
