# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('n1', models.IntegerField(verbose_name='Number-1')),
                ('n2', models.IntegerField(verbose_name='Number-2')),
                ('n3', models.IntegerField(verbose_name='Number-3')),
                ('n4', models.IntegerField(verbose_name='Number-4')),
                ('n5', models.IntegerField(verbose_name='Number-5')),
                ('n6', models.IntegerField(verbose_name='Number-6')),
                ('win', models.BooleanField(default=False, verbose_name='Win')),
                ('date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
