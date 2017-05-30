# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-30 17:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('C', 'creator'), ('D', 'developer')], max_length=1),
        ),
        migrations.AlterField(
            model_name='task',
            name='stage',
            field=models.CharField(choices=[('W', 'waiting'), ('P', 'in process'), ('F', 'failed'), ('D', 'done')], default='W', max_length=1),
        ),
    ]
