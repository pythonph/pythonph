# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20150106_2010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='job',
            name='slug',
        ),
    ]
