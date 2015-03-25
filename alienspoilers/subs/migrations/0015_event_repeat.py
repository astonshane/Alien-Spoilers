# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subs', '0014_event_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='repeat',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
