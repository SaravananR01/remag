# Generated by Django 5.0.3 on 2024-04-17 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all', '0005_merge_20240417_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='total_cost',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
