# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_job_application_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='application_email',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='job',
            name='application_url',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
    ]
