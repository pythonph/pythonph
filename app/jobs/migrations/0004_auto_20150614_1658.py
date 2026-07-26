# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_auto_20150614_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='application_email',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='application_url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
