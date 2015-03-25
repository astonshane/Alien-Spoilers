# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subs', '0015_event_repeat'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='repeat_type',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
    ]
