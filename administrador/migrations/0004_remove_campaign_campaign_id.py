# Generated by Django 5.1.5 on 2025-03-23 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrador', '0003_remove_campaign_publico_objetivo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='campaign_id',
        ),
    ]
