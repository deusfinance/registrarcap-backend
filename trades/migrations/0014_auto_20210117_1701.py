# Generated by Django 2.2 on 2021-01-17 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0013_auto_20210112_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='deus_price',
            field=models.DecimalField(decimal_places=18, default=0, max_digits=38),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trade',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trades', to='trades.Currency'),
        ),
    ]
