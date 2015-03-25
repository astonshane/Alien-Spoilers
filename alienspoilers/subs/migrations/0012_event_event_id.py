# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subs', '0011_event_subreddit_fullname'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_id',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
    ]
