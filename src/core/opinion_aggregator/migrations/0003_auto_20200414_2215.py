# Generated by Django 2.2.8 on 2020-04-14 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('opinion_aggregator', '0002_auto_20200414_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optionmodel',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='opinion_aggregator.QuestionModel'),
        ),
    ]