# Generated by Django 2.2.8 on 2020-04-23 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opinion_aggregator', '0007_auto_20200423_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='optionsubcategory',
            name='question',
        ),
    ]
