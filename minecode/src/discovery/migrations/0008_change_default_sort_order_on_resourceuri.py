# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-08 15:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('discovery', '0007_change_unique_constraints_on_resourceuri'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resourceuri',
            options={'ordering': ['canonical', '-last_visit_date'], 'verbose_name': 'Resource URI'},
        ),
    ]
