# Generated by Django 5.0.1 on 2024-04-16 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all', '0003_alter_company_c_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='department',
            field=models.CharField(default='tech', max_length=30),
            preserve_default=False,
        ),
    ]
