# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subs', '0009_auto_20150223_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='token_expiry',
            field=models.DateTimeField(null=True, verbose_name=b'token expiry'),
            preserve_default=True,
        ),
    ]
