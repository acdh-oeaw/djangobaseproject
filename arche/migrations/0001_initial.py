# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-20 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_title', models.CharField(blank=True, help_text='Title or name of Collection.', max_length=250, verbose_name='acdh:hasTitle')),
                ('description', models.TextField(blank=True, help_text='A verbose description of certain aspects of an entity.         This is the most generic property, use more specific sub-properties where applicable.', null=True, verbose_name='acdh:hasDescription')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_title', models.CharField(blank=True, help_text='Title or name of Collection.', max_length=250, verbose_name='acdh:hasTitle')),
                ('description', models.TextField(blank=True, help_text='A verbose description of certain aspects of an entity.         This is the most generic property, use more specific sub-properties where applicable.', null=True, verbose_name='acdh:hasDescription')),
                ('has_start_date', models.DateField(blank=True, help_text='Indicates the start date of a Project.', null=True, verbose_name='acdh:hasStartDate')),
                ('has_end_date', models.DateField(blank=True, help_text='Indicates the end date of a Project.', null=True, verbose_name='acdh:hasEndtDate')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
