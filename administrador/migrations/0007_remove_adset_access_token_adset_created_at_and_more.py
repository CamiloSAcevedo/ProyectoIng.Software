# Generated by Django 5.1.5 on 2025-03-26 01:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0006_ad_adset_remove_campaign_budget_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adset',
            name='access_token',
        ),
        migrations.AddField(
            model_name='adset',
            name='created_at',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='adset',
            name='status',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
