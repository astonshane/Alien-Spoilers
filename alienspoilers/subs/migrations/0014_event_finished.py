# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subs', '0013_auto_20150325_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='finished',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
