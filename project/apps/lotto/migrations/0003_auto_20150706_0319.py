# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lotto', '0002_auto_20150705_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='win',
            field=models.IntegerField(blank=True, verbose_name='Win', default=0),
        ),
    ]
