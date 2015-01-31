# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_markdown.models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20150108_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='profile',
            field=django_markdown.models.MarkdownField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='description',
            field=django_markdown.models.MarkdownField(),
            preserve_default=True,
        ),
    ]
