# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_auto_20150625_0141'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='is_sponsored',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
