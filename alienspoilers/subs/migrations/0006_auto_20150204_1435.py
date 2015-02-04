# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subs', '0005_auto_20150204_1432'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='reddit_linked',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='reddit_refresh_token',
        ),
    ]
