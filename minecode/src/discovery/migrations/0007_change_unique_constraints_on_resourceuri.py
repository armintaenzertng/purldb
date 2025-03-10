# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-08 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discovery', '0006_remove_resourceuri_metadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourceuri',
            name='canonical',
            field=models.CharField(db_index=True, help_text='Canonical form of the URI for this resource that must be unique across all ResourceURI.', max_length=3000),
        ),
        migrations.AlterUniqueTogether(
            name='resourceuri',
            unique_together=set([('canonical', 'last_visit_date')]),
        ),
    ]
