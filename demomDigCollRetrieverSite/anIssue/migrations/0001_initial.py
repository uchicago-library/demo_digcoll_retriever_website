# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-20 15:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0039_collectionviewrestriction'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnIssuePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('volume', models.CharField(blank=True, max_length=50, null=True)),
                ('issue', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='PageImageOrderable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page_url', models.URLField()),
                ('page_number', models.IntegerField()),
                ('issue', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_pages', to='anIssue.AnIssuePage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_title', models.CharField(max_length=255)),
                ('publication_description', wagtail.wagtailcore.fields.RichTextField()),
            ],
        ),
        migrations.CreateModel(
            name='PublicationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publication_type', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='publication',
            name='the_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='anIssue.PublicationType'),
        ),
        migrations.AddField(
            model_name='anissuepage',
            name='issue_publication',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='anIssue.Publication'),
        ),
    ]
