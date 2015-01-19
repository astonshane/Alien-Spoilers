# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Single_Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('subreddit', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('start_date', models.DateTimeField(verbose_name=b'start date')),
                ('end_date', models.DateTimeField(verbose_name=b'end date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
