# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-26 12:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xptracker', '0007_work_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='iteration',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='xptracker.Iteration'),
        ),
    ]
