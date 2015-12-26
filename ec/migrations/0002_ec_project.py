# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EC_Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_name', models.CharField(max_length=100)),
                ('project_type', models.IntegerField(default=1, choices=[(0, b'src'), (1, b'data')])),
            ],
        ),
    ]
