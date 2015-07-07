# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lotto', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ['-date', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6']},
        ),
        migrations.AddField(
            model_name='ticket',
            name='checked',
            field=models.BooleanField(verbose_name='Checked', default=False),
        ),
    ]
