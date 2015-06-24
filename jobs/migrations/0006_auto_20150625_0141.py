# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_auto_20150614_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='is_approved',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='company',
            name='user',
            field=models.ForeignKey(related_name='companies', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
