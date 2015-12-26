# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0003_auto_20151127_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='EC_Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('schedule_name', models.CharField(max_length=100)),
                ('schedule_enable', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='EC_Schedule_Backup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_restore', models.BooleanField(default=False)),
                ('backup_time', models.DateTimeField()),
                ('host', models.ForeignKey(related_name='schedule_host', to='ec.EC_Host')),
                ('project', models.ForeignKey(related_name='schedule_project', to='ec.EC_Project')),
            ],
        ),
        migrations.AddField(
            model_name='ec_schedule',
            name='backup',
            field=models.ForeignKey(related_name='schedule_backup', to='ec.EC_Schedule_Backup'),
        ),
    ]
