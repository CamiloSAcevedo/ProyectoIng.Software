# Generated by Django 5.1.5 on 2025-04-06 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0014_remove_ad_creative_ad_creative_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='access_token',
        ),
        migrations.AlterField(
            model_name='ad',
            name='adset_id',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='ad',
            name='creative_id',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
