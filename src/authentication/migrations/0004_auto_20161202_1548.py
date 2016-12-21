# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-02 15:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20161202_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='access_level_code',
            field=models.IntegerField(default=-1, help_text='1 stands for Inspector and 2 stands for Headmaster'),
        ),
        migrations.AlterField(
            model_name='account',
            name='school_three',
            field=models.ForeignKey(blank=True, default=-1, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='thirds', to='subject.Subject'),
        ),
        migrations.AlterField(
            model_name='account',
            name='subject_two',
            field=models.ForeignKey(blank=True, default=-1, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='seconds', to='subject.Subject'),
        ),
    ]