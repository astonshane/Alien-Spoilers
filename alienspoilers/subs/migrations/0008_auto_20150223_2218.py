# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subs', '0007_auto_20150204_1447'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='reddit_refresh_token',
            new_name='access_token',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='refresh_token',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
    ]
