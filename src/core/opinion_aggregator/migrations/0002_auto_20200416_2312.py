# Generated by Django 2.2.8 on 2020-04-16 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opinion_aggregator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionoptions',
            name='expected_answers',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='questionoptions',
            name='open_ended',
            field=models.BooleanField(default=False, help_text='Designates whether this question expects multiple answers.', verbose_name='open_ended'),
        ),
    ]
