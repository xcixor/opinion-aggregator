# Generated by Django 2.2.8 on 2020-04-25 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opinion_aggregator', '0009_surveyresponsesmodel_question_option'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveyresponsesmodel',
            name='question_option',
        ),
    ]
