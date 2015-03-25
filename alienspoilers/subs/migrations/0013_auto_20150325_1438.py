# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('subs', '0012_event_event_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_id',
            field=models.CharField(default=datetime.datetime(2015, 3, 25, 18, 38, 45, 179141, tzinfo=utc), max_length=200),
            preserve_default=False,
        ),
    ]
