# Generated by Django 4.2 on 2024-05-23 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('validator', '0005_causes_root_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='causes',
            name='feedback',
            field=models.CharField(default='', max_length=50),
        ),
    ]
