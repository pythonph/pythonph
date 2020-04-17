# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
from django.conf import settings
from markdownx import models as mdx_models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('profile', mdx_models.MarkdownxField()),
                ('homepage', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                (
                    'user',
                    models.ForeignKey(
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
            ],
            options={
                'verbose_name_plural': 'companies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('description', mdx_models.MarkdownxField()),
                ('location', models.CharField(max_length=255)),
                ('application_url', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                (
                    'company',
                    models.ForeignKey(
                        to='jobs.Company',
                        on_delete=models.CASCADE,
                    )
                ),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', help_text='A comma-separated list of tags.', verbose_name='Tags', through='taggit.TaggedItem')),
                (
                    'user',
                    models.ForeignKey(
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
