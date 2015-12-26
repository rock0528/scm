# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ec', '0002_ec_project'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ec_host',
            old_name='url',
            new_name='host_name',
        ),
    ]
