# Generated by Django 2.2 on 2021-01-12 06:25

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0011_trade_other'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='other',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
