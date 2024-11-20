# Generated by Django 5.0.6 on 2024-11-19 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_rename_correct_option_question_correct_answer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diya',
            name='x_coordinate',
        ),
        migrations.RemoveField(
            model_name='diya',
            name='y_coordinate',
        ),
        migrations.AddField(
            model_name='diya',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='diya',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
    ]
